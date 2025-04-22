from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView, CustomProviderAuthView,
    LogoutView,
    ProfileView, FarmerViewSet, CustomUserViewSet, test, EmployeeViewSet
)

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'farmers', FarmerViewSet, basename='farmer')
router.register(r'employees', EmployeeViewSet, basename='employee')


urlpatterns = [
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView),
    path('profiles/', ProfileView.as_view()),
    path('', include(router.urls)),
    
    path('test/', test )
]
