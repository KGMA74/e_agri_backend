from rest_framework import serializers
from djoser.serializers import UserSerializer
from .models import Profile, Farmer, Employee
from django.contrib.auth import get_user_model

User = get_user_model()
class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('role', 'profile', 'farmer', 'employee')
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        request = self.context.get('request')
        if request and request.method in ['GET', 'POST']:
            data['profile'] = ProfileSerializer(instance.profile, many=False).data
            
            if getattr(instance, 'farmer', None):
                data['farmer'] = FarmerSerializer(instance.farmer, many=False).data
            if getattr(instance, 'employee', None):
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



class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'firstname', 'lastname', 'password', 're_password', 'role']

    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({"re_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('re_password')  # On retire le champ inutilisé
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class EmployeeCreateSerializer(serializers.ModelSerializer):
    user_data = CustomUserCreateSerializer(write_only=True)

    class Meta:
        model = Employee
        fields = ['user_data', 'salary', 'post']

    def create(self, validated_data):
        user_data = validated_data.pop('user_data')
        user_data['role'] = 'employee'  # Forcer le rôle

        user_serializer = CustomUserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        employee = Employee.objects.create(user=user, **validated_data)
        return employee

    def to_representation(self, instance):
        return EmployeeSerializer(instance, context=self.context).data
