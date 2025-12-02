from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Asset, Category
from .serializers import AssetSerializer, CategorySerializer
from users.permissions import IsAdmin 

User = get_user_model()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin] # Only Admins can edit Categories

class AssetViewSet(viewsets.ModelViewSet):
    # --- THIS WAS MISSING ---
    queryset = Asset.objects.all().select_related('category', 'assigned_to')
    serializer_class = AssetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'serial_number', 'assigned_to__email']
    # ------------------------

    def get_permissions(self):
        """
        Custom Logic:
        - Listing/Retrieving: Allowed for any Authenticated User (Employees)
        - Creating/Deleting/Checkout/Return: Only Admins
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    # === Custom Action: CHECKOUT ===
    @action(detail=True, methods=['post'], url_path='checkout')
    def checkout(self, request, pk=None):
        asset = self.get_object()
        employee_id = request.data.get('employee_id')

        # 1. Validation: Is it available?
        if asset.status != Asset.Status.AVAILABLE:
            return Response(
                {"error": f"Asset is currently {asset.status}. Cannot check out."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Validation: Did they send an Employee ID?
        if not employee_id:
            return Response(
                {"error": "employee_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Perform the Action
        employee = get_object_or_404(User, id=employee_id)
        asset.assigned_to = employee
        asset.status = Asset.Status.ASSIGNED
        asset.save() 

        return Response({
            "status": "success", 
            "message": f"Asset assigned to {employee.email}"
        })

    # === Custom Action: RETURN ===
    @action(detail=True, methods=['post'], url_path='return')
    def return_asset(self, request, pk=None):
        asset = self.get_object()

        # 1. Validation: Is it actually assigned?
        if asset.status != Asset.Status.ASSIGNED:
            return Response(
                {"error": "Asset is not currently assigned."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Perform the Action
        asset.assigned_to = None
        asset.status = Asset.Status.AVAILABLE
        asset.save() 

        return Response({"status": "success", "message": "Asset returned to pool"})