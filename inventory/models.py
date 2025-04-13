from django.db import models

# Create your models here.
class Inventory(models.Model):
    pass

class Equipment(models.Model):
    inventory = models.ForeignKey('Inventory', related_name='equipements', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)

class Fertilizer(models.Model):
    inventory = models.ForeignKey('Inventory', related_name='fertilizers', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    quantity = models.FloatField()
    type = models.CharField(max_length=20)

class Seeds(models.Model):
    inventory = models.ForeignKey('Inventory', related_name='seeds', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    quantity = models.FloatField()
    type = models.CharField(max_length=20)
    