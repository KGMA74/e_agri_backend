from django.contrib import admin
from .models import User, Employee, Farmer
# Register your models here.

admin.site.register([
    User,
    Farmer,
    Employee
])
