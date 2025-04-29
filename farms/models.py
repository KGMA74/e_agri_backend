from django.db import models
from core.models import BaseModel

# Create your models here.
class Farm(BaseModel):
    owner = models.ForeignKey('accounts.Farmer', related_name='farms', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    area = models.FloatField(help_text="superficie en hectares", default=0)
    location = models.CharField(max_length=100) #  coord geographique ou le vilage
    
    def __str__(self):
        return f"Field {self.name} @{self.location} owner: {self.owner.user}"
    
class Field(models.Model):
    farm = models.ForeignKey("Farm", related_name='fields', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    area = models.FloatField(help_text="superficie en hectares", default=0)
  

class Crop(models.Model): # culture
    STATUS_CHOICES = [
        ('done', 'Done'),
    ]
    name = models.CharField(max_length=20) # mais, ble, ....
    variety = models.CharField(max_length=100, blank=True)
    growth_duration = models.IntegerField(help_text="Durée de croissance en jours", default='30')

    def __str__(self):
        return f"{self.name} ({self.variety})"
    
class Planting(models.Model): # pour suivre les plantation
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="plantings")
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="plantings")
    planting_date = models.DateField()
    expected_harvest_date = models.DateField() # date previsionnelle pour la recolte
    seed_quantity = models.FloatField(help_text="Quantité en kg")
    
    def __str__(self):
        return f"{self.crop.name} - {self.field.name}"

class Harvest(models.Model):
    harvest_date = models.DateTimeField()
    yield_amount = models.FloatField(help_text='rendement en tonnes')
    quality_rating = models.IntegerField(choices=[
        (1, 'Faible'),
        (2, 'Moyen'),
        (3, 'Eleve')
    ])
    
    def __str__(self):
        return f"Récolte du {self.harvest_date} ({self.yield_amount} tonnes)"