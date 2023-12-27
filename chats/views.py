from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import SingleUserRoom, ChatMessage

# Create your views here.
@login_required
def chat_index(request):

    chats = SingleUserRoom.get_user_rooms(request.user)
    return render(request, 'chats/index.html', {"chats" : chats})



@login_required
def get_chatroom_message(request, chatroom_id):
    try:
        chatroom = SingleUserRoom.objects.get(pk=chatroom_id)
        messages = ChatMessage.objects.filter(chatroom=chatroom)

    except:
        return HttpResponse('Server error!')