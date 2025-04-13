from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('alert', 'Alert'),
        ('task', 'Task'),
        ('message', 'Message'),
        ('system', 'System'),
    ]
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} - {self.notification_type}"

    class Meta:
        ordering = ['-date_sent']
