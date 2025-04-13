from django.db import models
from core.models import BaseModel

# Create your models here.
class Farm(BaseModel):
    owner = models.ForeignKey('accounts.Farmer', related_name='farms', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=100) #  coord geographique ou le vilage
    
    def __str__(self):
        return f"Field {self.name} @{self.location} owner: {self.owner.user}"
    
class Field(models.Model):
    farm = models.ForeignKey("Farm", related_name='fields', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    size = models.FloatField() # en ha
    
    def addCrop():
        pass
    
    def removeCrop():
        pass
    
    def viewCropDetails():
        pass
    
    def updateFieldDetails():
        pass
    
    
class Crop(models.Model):
    STATUS_CHOICES = [
        ('done', 'Done'),
    ]
    
    field = models.ForeignKey('Field', related_name='crops', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    plantingDate = models.DateTimeField()
    harvestDate = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='done')
    