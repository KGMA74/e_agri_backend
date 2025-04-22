import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.room_group_name = f'notifications_{self.user.id}'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        # Vérifie si l'action concerne la mise à jour d'une notification comme lue
        if 'mark_as_read' in text_data_json:
            notification_id = text_data_json['mark_as_read']
            await self.mark_notification_as_read(notification_id)

        message = text_data_json.get('message')
        
        if message:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'notification_message',
                    'message': message
                }
            )

    async def notification_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @staticmethod
    def create_notification(user, message, notification_type):
        notification = Notification.objects.create(
            user=user,
            message=message,
            notification_type=notification_type,
        )
        
        # Envoi de la notification en temps réel via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_{user.id}',
            {
                'type': 'notification_message',
                'message': message,
                'notification_id': notification.id
            }
        )

    @sync_to_async
    def mark_notification_as_read(self, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
        except Notification.DoesNotExist:
            pass  # Si la notification n'existe pas, on ignore
