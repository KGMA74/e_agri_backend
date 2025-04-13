from rest_framework import serializers
from djoser.serializers import UserSerializer
from .models import Profile, Farmer, Employee

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('role', 'profile', 'teacher', 'student', 'parent')
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        request = self.context.get('request')
        if request and request.method in ['GET']:
            data['profile'] = ProfileSerializer(instance.profile, many=False).data
            
            if getattr(instance, 'farmer', None):
                data['farmer'] = FarmerSerializer(instance.farmer, many=False).data
            if getattr(instance, 'emplyee', None):
                data['employee'] = EmployeeSerializer(instance.employee, many=False).data
                
        return data

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        request = self.context.get('request')
        if request and request.method in ['GET']:
            data['user'] = CustomUserSerializer(instance.user, many=False).data
        
        return data
    

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        request = self.context.get('request')
        if request and request.method in ['GET']:
            data['user'] = CustomUserSerializer(instance.user, many=False).data
        
        return data