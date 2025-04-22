from django.contrib import admin
from .models import WeatherData, DiseaseAlert


# Register your models here.
admin.site.register([
    WeatherData,
    DiseaseAlert
])