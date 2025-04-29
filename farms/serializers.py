from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Farm, Crop, Field

class FarmSerializer(ModelSerializer):
    class Meta:
        model = Farm
        fields = '__all__'
        
class FieldSerializer(ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'
        
    def validate(self, attrs):
        if attrs['size'] < 0:
            raise ValidationError({'size': 'size must be non-negative'})
        return super().validate(attrs)
    
class CropSerializer(ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'