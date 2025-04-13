from django.db import models

# Create your models here.
#Dans une autre app

class Expense(models.Model):
    farm = models.ForeignKey('farms.Farm', related_name='expenses', on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    
    def addExpense():
        pass
    
class Revenue(models.Model):
    farm = models.ForeignKey('farms.Farm', related_name='revenues', on_delete=models.CASCADE)
    source = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    
    def addRevenue():
        pass