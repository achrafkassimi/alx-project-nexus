import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Message
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.user_id = int(self.scope['url_route']['kwargs']['user_id'])
        self.user = self.scope["user"]
        
        # Create consistent room name regardless of user order
        self.room_group_name = f"chat_{min(self.user.id, self.user_id)}_{max(self.user.id, self.user_id)}"

        print(f"User {self.user.username} connecting to room {self.room_group_name}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print(f"User {self.user.username} disconnecting from room {self.room_group_name}")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(f"Received message: {text_data}")
        
        try:
            data = json.loads(text_data)
            message = data['message']
            sender = self.scope['user']
            receiver_id = self.user_id

            # Save message to database
            msg = await self.save_message(sender, receiver_id, message)
            print(f"Message saved: {msg.id}")

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': msg.content,
                    'sender': sender.username,
                    'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
            print(f"Message broadcasted to room {self.room_group_name}")
            
        except Exception as e:
            print(f"Error in receive: {e}")

    async def chat_message(self, event):
        print(f"Broadcasting message to WebSocket: {event}")
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def save_message(self, sender, receiver_id, content):
        from users.models import CustomUser
        receiver = CustomUser.objects.get(id=receiver_id)
        return Message.objects.create(sender=sender, receiver=receiver, content=content)