import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from .models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'notifications_44'
        self.user = self.scope['user']
        if self.user.is_authenticated:
            # self.room_group_name = f'notifications_{self.user.id}'
            
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.channel_layer.group_add(
                'notifications_44',
                self.channel_name
            )
            await self.accept()
            
        await self.channel_layer.group_send(
            'notifications_44',
            {
                'type': 'send_notification',
                'message': 'connecte avec success'
            }
        )
            # await self.close()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
        
    #     # Vérifie si l'action concerne la mise à jour d'une notification comme lue
    #     if 'mark_as_read' in text_data_json:
    #         notification_id = text_data_json['mark_as_read']
    #         await self.mark_notification_as_read(notification_id)

    #     message = text_data_json.get('message')
        
    #     if message:
    #         await self.channel_layer.group_send(
    #             # self.group_name,
    #             'notifications_44',
    #             {
    #                 'type': 'send_notification',
    #                 'message': message
    #             }
    #         )

    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @staticmethod
    def create_notification(user, message, notification_type):
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
              'notifications_44',
            {
                'type': 'send_notification',
                'message': message,
                # 'notification_id': notification.id
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

# 
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from .models import Notification


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        if not self.user.is_authenticated:
            await self.close()
            return

        self.group_name = f'notifications_{self.user.id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

        # Envoyer un message de confirmation
        await self.send(text_data=json.dumps({
            'type': 'connection',
            'message': 'Connecté avec succès'
        }))

        # Envoyer les anciennes notifications non lues
        await self.send_old_notifications()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Marquer une notification comme lue
        if 'mark_as_read' in data:
            await self.mark_notification_as_read(data['mark_as_read'])

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_notification',
            'message': event['message']
        }))

    async def send_old_notifications(self):
        notifications = await self.get_old_notifications()
        for notif in notifications:
            await self.send(text_data=json.dumps({
                'type': 'old_notification',
                'message': notif.content,
                'created_at': notif.created_at.isoformat()
            }))

    @sync_to_async
    def get_old_notifications(self):
        return Notification.objects.filter(receiver=self.user, is_read=False).order_by('-created_at')[:10]

    @sync_to_async
    def mark_notification_as_read(self, notification_id):
        try:
            notif = Notification.objects.get(id=notification_id, receiver=self.user)
            notif.is_read = True
            notif.save()
        except Notification.DoesNotExist:
            pass

    @staticmethod
    def create_notification(receiver, message):
        channel_layer = get_channel_layer()
        group_name = f'notifications_{receiver.id}'

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_notification',
                'message': message
            }
        )
