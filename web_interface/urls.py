from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Asset Actions
    path('asset/<uuid:asset_id>/checkout/', views.checkout_asset, name='web_checkout'),
    path('asset/<uuid:asset_id>/return/', views.return_asset, name='web_return'),
    
    # Admin Create Actions
    path('add_employee/', views.add_employee, name='add_employee'),
    path('add_asset/', views.add_asset, name='add_asset'),

    # Admin Delete Actions
    path('delete_asset/<uuid:asset_id>/', views.delete_asset, name='delete_asset'),
    path('delete_employee/<int:user_id>/', views.delete_employee, name='delete_employee'),
]