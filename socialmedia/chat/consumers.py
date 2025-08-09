import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user_id = int(self.scope['url_route']['kwargs']['user_id'])
        self.user = self.scope["user"]
        self.room_group_name = f"chat_{min(self.user.id, self.user_id)}_{max(self.user.id, self.user_id)}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user']
        receiver_id = self.user_id

        # Save message to database
        msg = await self.save_message(sender, receiver_id, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg.content,
                'sender': sender.username,  # This should match frontend expectation
                'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],  # Make sure this matches frontend
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def save_message(self, sender, receiver_id, content):
        return Message.objects.create(sender=sender, receiver_id=receiver_id, content=content)