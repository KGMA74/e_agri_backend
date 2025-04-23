from .models import Farm, Crop, Field
from .serializers import FarmSerializer, FieldSerializer, CropSerializer
from rest_framework.viewsets import ModelViewSet
from accounts.permissions import IsAdminOrFarmerOrReadOnly
# Create your views here.

class FarmViewSet(ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    permission_classes = [IsAdminOrFarmerOrReadOnly]