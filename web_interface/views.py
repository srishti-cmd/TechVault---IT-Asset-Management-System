from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib import messages
from inventory.models import Asset, Category
from users.models import User

# --- Helper ---
def is_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'

class CustomLoginView(LoginView):
    template_name = 'web_interface/login.html'

@login_required
def dashboard(request):
    user = request.user
    
    # 1. FETCH ALL DATA
    all_assets = Asset.objects.all().select_related('category', 'assigned_to').order_by('-created_at')
    all_users = User.objects.all().order_by('-created_at') 
    employees = User.objects.filter(role='EMPLOYEE') 
    categories = Category.objects.all()
    
    # 2. PERSONAL ASSETS
    my_assets = Asset.objects.filter(assigned_to=user)

    # 3. CALCULATE STATS
    stats = {
        'total': all_assets.count(),
        'assigned': all_assets.filter(status='ASSIGNED').count(),
        'available': all_assets.filter(status='AVAILABLE').count(),
        'broken': all_assets.filter(status='BROKEN').count(),
        'user_count': all_users.count()
    }

    # 4. GRAPH DATA
    graph_labels = []
    graph_data = []
    for cat in categories:
        count = all_assets.filter(category=cat).count()
        if count > 0:
            graph_labels.append(cat.name)
            graph_data.append(count)

    context = {
        'assets': all_assets,      
        'my_assets': my_assets,    
        'all_users': all_users,    
        'employees': employees,
        'categories': categories,  # <--- THIS LINE WAS MISSING!
        'stats': stats,
        'graph_labels': graph_labels,
        'graph_data': graph_data,
        'is_admin': user.role == 'ADMIN' 
    }
    return render(request, 'web_interface/dashboard.html', context)

# --- ACTIONS (Direct Assignment) ---
@login_required
def checkout_asset(request, asset_id):
    if request.user.role != 'ADMIN':
        messages.error(request, "Permission Denied: Only Admins can assign assets.")
        return redirect('dashboard')

    if request.method == 'POST':
        asset = get_object_or_404(Asset, id=asset_id)
        employee_id = request.POST.get('employee_id')
        
        # VALIDATION: Only assign if Available
        if asset.status == 'AVAILABLE' and employee_id:
            employee = User.objects.get(id=employee_id)
            
            # DIRECT ASSIGNMENT (No Email, No Pending)
            asset.assigned_to = employee
            asset.status = 'ASSIGNED'
            asset.save() # Triggers Ghost Audit Log
            
            messages.success(request, f"Asset successfully assigned to {employee.first_name}.")
        else:
            messages.error(request, "Could not checkout asset.")
            
    return redirect('dashboard')

@login_required
def return_asset(request, asset_id):
    if request.user.role != 'ADMIN':
        messages.error(request, "Permission Denied: Only Admins can return assets.")
        return redirect('dashboard')

    if request.method == 'POST':
        asset = get_object_or_404(Asset, id=asset_id)
        if asset.status == 'ASSIGNED':
            asset.assigned_to = None
            asset.status = 'AVAILABLE'
            asset.save() # Triggers Ghost Audit Log
            messages.success(request, "Asset returned to pool.")
    return redirect('dashboard')

# --- CREATE ACTIONS ---
@login_required
@user_passes_test(is_admin)
def add_employee(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "User already exists.")
        else:
            User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, role='EMPLOYEE')
            messages.success(request, "Employee added.")
    return redirect('dashboard')

@login_required
@user_passes_test(is_admin)
def add_asset(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        serial = request.POST.get('serial')
        category_id = request.POST.get('category')
        cat = Category.objects.get(id=category_id)
        
        if Asset.objects.filter(serial_number=serial).exists():
            messages.error(request, "Serial Number must be unique.")
        else:
            Asset.objects.create(name=name, serial_number=serial, category=cat)
            messages.success(request, "Asset created.")
    return redirect('dashboard')

# --- DELETE ACTIONS ---
@login_required
@user_passes_test(is_admin)
def delete_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    name = asset.name
    asset.delete()
    messages.success(request, f"Asset '{name}' deleted permanently.")
    return redirect('dashboard')

@login_required
@user_passes_test(is_admin)
def delete_employee(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.error(request, "You cannot delete yourself!")
    else:
        user.delete()
        messages.success(request, "User deleted.")
    return redirect('dashboard')