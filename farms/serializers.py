from rest_framework.serializers import ModelSerializer
from .models import Farm, Crop, Field

class FarmSerializer(ModelSerializer):
    class Meta:
        model = Farm
        fields = '__all__'
        
class FieldSerializer(ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'
        
class CropSerializer(ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'