from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from .manager import UserManager
from core.models import BaseModel

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    
    ROLE_CHOICES = [
        ('farmer','Farmer'),
        ('employee','Employee'),
        ('admin','Admin')
    ]
    
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=50)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='farmer')    

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'role']

    def __str__(self):
        return self.email
    
    def has_module_perms(self, obj=None):
        return self.is_staff
    
    def has_perm(self, perm, obj=None):
        return True
    
    @property
    def fullname(self):
        return f"{self.firstname} {self.lastname}"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.fullname}"

# === User Specialization === #
class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer', primary_key=True)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee', primary_key=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='employees')
    tasks = models.ManyToManyField('tasks.Task', related_name='employees')
    salary = models.FloatField(default=0.)
    post = models.CharField(max_length=50)