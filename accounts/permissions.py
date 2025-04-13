from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.User and request.user.is_superuser
    
    
class IsAdminOrFarmer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.User and (request.user.is_superuser or request.user.role == 'farmer')