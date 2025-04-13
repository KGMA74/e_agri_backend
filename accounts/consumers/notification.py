

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from django.contrib.auth import get_user_model



# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#        self.room_name = self.scope['url_route']['kwargs']['room_name'] 
#        self.room_group_name = f'chat_{self.room_name}'
       
#        #join room
#        await self.channel_layer.group_add(
#            self.room_group_name,
#            self.room_name
#        )
       
#        await self.accept()
       
#     async def disconnect(self, code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.room_name
#         )
        
#     async def receive(self, text_data):
#         data = json.loads(text_data)['data']
        
#         converse_id = data['conversation_id']
        
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message'
#             }
#         )
        
#     async def chat_mesasage(self, event):
#         name = event['name']
#         body = event['body']
        
#         await self.send(text_data=json.dumps({
#             'body': body,
#             'name': name
#         }))
        
#         @sync_to_async
#         def save_message(self, conversation_id, body):
#             user = self.scope['user']
#             Message.object.create(
                
#             )