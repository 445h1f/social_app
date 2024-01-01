from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import ChatMessage, SingleUserRoom
from django.contrib.auth import get_user_model
from users.models import Profile

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    # method for connecting to websocket
    async def connect(self):
        self.websocket_name = 'chatrooms'

        await self.channel_layer.group_add(
            self.websocket_name,
            self.channel_name,
        )

        await self.accept()


    # method to disconnect
    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.websocket_name,
            self.channel_name,
        )

    @database_sync_to_async
    def save_message_to_database(self, message, user, chatroom):
        msg_save = ChatMessage(body=message, user=user, chatroom=chatroom)
        msg_save.save()

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_user_profile_image(self, user):
        return Profile.objects.get(user=user).image.url

    @database_sync_to_async
    def get_chatroom_by_id(self, room_id):
        return SingleUserRoom.objects.get(id=room_id)


    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        room_id = data['chatroom_id']
        user_id = data['user_id']

        # Use async versions of synchronous database calls
        user = await self.get_user_by_id(user_id)
        chatroom = await self.get_chatroom_by_id(room_id)
        user_image = await self.get_user_profile_image(user)

        # Save the message to the database asynchronously
        await self.save_message_to_database(message, user, chatroom)

        await self.channel_layer.group_send(
            self.websocket_name,
            {
                'type' : 'chat_message',
                'message' : message,
                'user_id' : user_id,
                'chatroom_id' : room_id,
                'user_image' : user_image
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        room_id = event['chatroom_id']
        user_image = event['user_image']

        await self.send(text_data=json.dumps({
            'message' : message,
            'user_id' : user_id,
            'chatroom_id' : room_id,
            'user_image' : user_image
        }))