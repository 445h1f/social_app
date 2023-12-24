from django.urls import path
from . import views as posts_views


urlpatterns = [
    path('create/', view=posts_views.create_post, name='create_post'),
    path('<int:post_id>', view=posts_views.view_post, name='view_post'),
    path('like', view=posts_views.like_post, name='like'),
    path('comment', view=posts_views.comment_post, name='comment'),
]