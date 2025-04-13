from rest_framework import serializers
from djoser.serializers import UserSerializer
from .models import Level, Profile, Student, Teacher, Parent, XPTransaction, Farmer, Employee

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('role', 'profile', 'teacher', 'student', 'parent')
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        request = self.context.get('request')
        if request and request.method in ['GET']:
            data['profile'] = ProfileSerializer(instance.profile, many=False).data
            
            if getattr(instance, 'farmer', None):
                data['farmer'] = ParentSerializer(instance.farmer, many=False).data
            if getattr(instance, 'emplyee', None):
                data['employee'] = TeacherSerializer(instance.employee, many=False).data
                
            # if getattr(instance, 'parent', None):
            #     data['parent'] = ParentSerializer(instance.parent, many=False).data
            # if getattr(instance, 'teacher', None):
            #     data['teacher'] = TeacherSerializer(instance.teacher, many=False).data
            # if getattr(instance, 'student', None):
            #     data['student'] = StudentSerializer(instance.student, many=False).data
            #     data['student']['level'] = LevelSerializer(instance.student.level, many=False).data
       
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

# ------------------------------delete
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        request = self.context.get('request')
        if request and request.method in ['GET']:
            data['user'] = CustomUserSerializer(instance.user, many=False).data
        
        return data
    
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level 
        fields = '__all__'
    
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        request = self.context.get('request')
        if request and request.method in ['GET']:
            data['user'] = CustomUserSerializer(instance.user, many=False).data
            data['level'] = LevelSerializer(instance.level, many=False).data
        
        return data


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        request = self.context.get('request')
        if request and request.method in ['GET']:
            data['user'] = CustomUserSerializer(instance.user, many=False).data
        
        return data

class EnrollCourseSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

class AddChildSerializer(serializers.Serializer):
    pass
    student_id = serializers.IntegerField()
    

class XPTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = XPTransaction
        fields = ['user', 'xp_points', 'reason', 'created_at']
        read_only_fields = ['user', 'created_at']


