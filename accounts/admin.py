from django.contrib import admin
from .models import User, Employee, Farmer, Profile
# Register your models here.

admin.site.register([
    User,
    Farmer,
    Employee,
    Profile
])
