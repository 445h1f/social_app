from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chatsocket/', ChatConsumer.as_asgi()),
]