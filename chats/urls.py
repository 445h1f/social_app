from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.chat_index, name='chat_index'),
]