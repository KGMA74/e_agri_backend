from django.db import models

# Create your models here.

# retrive those data from a wheather api
class WeatherData(models.Model):
    farm = models.ForeignKey('farms.Farm', related_name='weatherData', on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    precipitation = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False)
    
class DiseaseAlert(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('middle', 'Middle'),
        ('higher', 'Higher'),
    ]
    
    farm = models.ForeignKey('farms.Farm', related_name='deseaseAlerts', on_delete=models.CASCADE)
    deseaseName = models.CharField(default="unkown", max_length=50)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    severity = models.CharField(max_length=50, choices=SEVERITY_CHOICES, default='low')