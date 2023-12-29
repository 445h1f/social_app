from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

# Create your models here.

# model for chat rooms for user to user
class SingleUserRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # user which created the chat room
    from_user = models.ForeignKey(User, on_delete=models.SET(None), related_name='chat_creator')
    # user to which it is created
    to_user = models.ForeignKey(User, on_delete=models.SET(None), related_name='chat_mate')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.from_user.username} - {self.to_user.username}'

    @staticmethod
    def get_user_rooms(user):
        return SingleUserRoom.objects.filter(
            models.Q(from_user=user) | models.Q(to_user=user)
        )


class ChatMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # user who sent the message
    user = models.ForeignKey(User, on_delete=models.SET(None), related_name='user_chat_message')
    body = models.TextField(max_length=5000)
    chatroom = models.ForeignKey(SingleUserRoom, on_delete=models.SET(None), related_name='message_room')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.chatroom} - {self.body[:50]}'