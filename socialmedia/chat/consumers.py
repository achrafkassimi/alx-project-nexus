import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Message

# chat/consumers.py
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
        # print("Received data on websocket:", text_data)  # تأكد أنه استقبل الرسالة

        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user']
        receiver_id = self.user_id  # خاص تحددها حسب room أو parameter


        # حفظ الرسالة فـ DB
        msg = await self.save_message(sender, receiver_id, message)

        # إرسال الرسالة للمجموعة
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': msg.content,
                'sender': sender.username,
                'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    async def chat_message(self, event):
        # print("Sending message to websocket:", event)
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def save_message(self, sender, receiver_id, content):
        return Message.objects.create(sender=sender, receiver_id=receiver_id, content=content)
    

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            "message": "✅ Connection established!"
        }))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({
            "message": f"Echo: {data.get('message')}"
        }))
