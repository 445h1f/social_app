from django.urls import path
from . import views as posts_views


urlpatterns = [
    path('create/', view=posts_views.create_post, name='create_post'),
    path('like', view=posts_views.like_post, name='like'),
]