from django.db import models

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('notStarted', 'NotStarted'),
        ('pending', 'Pending'),
        ('done', 'Done'),
    ]
    farm = models.ForeignKey('farms.Farm', related_name='tasks', on_delete=models.CASCADE)
    description = models.TextField()
    dueDate = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='notStarted')
    