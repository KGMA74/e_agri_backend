from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView, LogoutView,
    ProfileViewSet, FarmerViewSet, CustomUserViewSet, test
)

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'farmers', FarmerViewSet, 'farmer')

urlpatterns = [
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    
    path('test/', test )
]
