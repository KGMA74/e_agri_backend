from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import FarmViewSet, FieldViewSet, CropViewSet

router = DefaultRouter()
router.register(r'farms', FarmViewSet, basename='farm')
router.register(r'fields', FieldViewSet, basename='field')
router.register(r'crops', CropViewSet, basename='crop')

urlpatterns = [
    path('', include(router.urls))
]
