from django.contrib import admin
from .models import SingleUserRoom, ChatMessage


# Register your models here.
admin.site.register(SingleUserRoom)
admin.site.register(ChatMessage)