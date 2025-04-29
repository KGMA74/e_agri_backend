from .models import Farm, Crop, Field
from .serializers import FarmSerializer, FieldSerializer, CropSerializer
from rest_framework.viewsets import ModelViewSet
from accounts.permissions import IsAdminOrFarmerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
# Create your views here.

class FarmViewSet(ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    permission_classes = [IsAdminOrFarmerOrReadOnly]
    
class FieldViewSet(ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated, IsAdminOrFarmerOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            with transaction.atomic():
                self.perform_create(serializer)
                owner = serializer.instance.farm.owner
                
                user = request.user
                if user.role == 'farmer' and owner.pk != user.pk:
                    raise Exception("vous n'avez pas les droits necessaires pour l'ajout de ce champ a cette ferme")
                
        except Exception as e:
            return Response(
                {"detail": f"Field registration failed >> {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class CropViewSet(ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticated, IsAdminOrFarmerOrReadOnly]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            with transaction.atomic():
                self.perform_create(serializer)
                owner = serializer.instance.field.farm.owner
                
                user = request.user
                if user.role == 'farmer' and owner.pk != user.pk:
                    raise Exception("vous n'avez pas les droits necessaires pour l'ajout de cette culture a cette ce champ")
                
        except Exception as e:
            return Response(
                {"detail": f"Crop registration failed >> {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
