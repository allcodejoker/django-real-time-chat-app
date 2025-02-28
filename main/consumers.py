from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message, Room
from django.contrib.auth.models import User
from datetime import datetime
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = f"chat_{self.room_code}"

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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        date_send = datetime.now().strftime('%H:%M:%S')

        room = await self.get_room(self.room_code)
        user = await self.get_user(username)

        if room and user:
            await self.create_message(room, user, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'username': username,
                    'message': message,
                    'date_send': date_send
                }
            )

    async def chat_message(self, event):
        username = event['username']
        message = event['message']
        date_send = event['date_send']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'username': username,
            'message': message,
            'date_send': date_send
        }))

    # Convert Django ORM queries to async-compatible functions
    @sync_to_async
    def get_room(self, room_code):
        return Room.objects.filter(code=room_code).first()

    @sync_to_async
    def get_user(self, username):
        return User.objects.filter(username=username).first()

    @sync_to_async
    def create_message(self, room, user, message):
        return Message.objects.create(room=room, user=user, context=message, date_send=datetime.now())
