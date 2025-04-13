from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from ..accounts.manager import UserManager
from core.models import BaseModel
from courses.models import Course

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    
    ROLE_CHOICES = [
        ('farmer','Farmer'),
        ('employee','Employee'),
        ('admin','Admin')
    ]
    
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=50)
    
    
    
    #la definition du champ password n'est pas necessaire car faite par defaut par django
    
    # createdt_a = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='emplyee', primary_key=True)
    
    
class Teacher(models.Model):

    specialty = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)

    def __str__(self):
        return f"Teacher: {self.user.fullname}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', primary_key=True)
    # birth_date = models.DateField()
    xp = models.IntegerField(default=0)
    level = models.ForeignKey("Level", on_delete=models.SET_NULL, default=1, null=True)

    def __str__(self):
        return f"Student: {self.user.lastname} ({self.user})"

    def enroll_in_course(self, course):
        if isinstance(course, Course) and course.min_level_required <= self.level:
            self.courses.add(course)
            return True
        return False

    def drop_course(self, course):
        if isinstance(course, Course):
            self.courses.remove(course)

    def get_courses(self):
        return self.courses.all()
    
    def update_level(self):
        """Met à jour le niveau de l'étudiant en fonction des XP accumulés."""
        levels = Level.objects.all().order_by('min_xp')  # Trie les niveaux par XP croissant
        for level in levels:
            if self.xp >= level.min_xp:
                self.level = level
            else:
                break
        self.save()
        
    def add_xp(self, points):
        """Ajoute des XP à l'élève et met à jour son niveau."""
        self.xp += points
        self.update_level()
    
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent', primary_key=True)
    children = models.ManyToManyField(Student, related_name='parents', blank=True)

    def __str__(self):
        return f"Parent: {self.user.fullname}"
    
    def add_child(self, child):
        if isinstance(child, Student):
            self.children.add(child)

    def remove_child(self, child):
        if isinstance(child, Student):
            self.children.remove(child)

    def get_children(self):
        return self.children.all()
    
class VerificationCode(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='verification_codes')
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='verification_requests')
    code = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)
        
    @property
    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()
    

        
        
class XPTransaction(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="xp_transactions")
    xp_points = models.IntegerField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} earned {self.xp_points} XP for {self.reason}"


class Level(models.Model):
    level = models.IntegerField(default=0, primary_key=True)
    min_xp = models.IntegerField()
    max_xp = models.IntegerField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Save first to ensure we have an ID
        super().save(*args, **kwargs)
        # Find the previous level and update its max_xp
        prev_level = Level.objects.filter(level__lt=self.level).order_by('-level').first()
        if prev_level:
            prev_level.max_xp = self.min_xp - 1
            prev_level.save(update_fields=['max_xp'])
            
    def __str__(self):
        max_xp_str = f" - {self.max_xp}" if self.max_xp is not None else "+"
        return f"Level {self.level} (XP: {self.min_xp}{max_xp_str})"