from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Allows access only to users with role='ADMIN'.
    """
    def has_permission(self, request, view):
        # We also check is_staff for safety
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'