from django.contrib import admin
from .models import Farm, Crop, Field

# Register your models here.
admin.site.register([
    Farm,
    Crop,
    Field
])
