from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .consumers import NotificationConsumer
from .models import Notification


User = get_user_model()


@receiver(post_save, sender=Notification)
def notify_user_on_task_notification(sender, instance, created, **kwargs):
    if created:
        NotificationConsumer.create_notification(
                notification_type='task',
                user = instance.user,
                message=instance.message
            )
        NotificationConsumer().send_notification(event={'message': instance.message})