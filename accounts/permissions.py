from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view)
    
    
class IsAdminOrFarmer(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return super().has_permission(request, view) or request.user.role == 'farmer'
    
class IsAdminOrFarmerOrReadOnly(IsAdminOrFarmer):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view)