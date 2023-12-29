from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import uuid

User = get_user_model()

# Create your models here.

# model for social media post by user
class Post(models.Model):
    # uuid as primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # user who created the post
    user = models.ForeignKey(User, on_delete=models.SET(None))

    #image if added with post
    image = models.ImageField(upload_to='post/%Y/%m/%d', blank=True)

    caption = models.TextField(blank=True)    # caption of image
    title = models.CharField(max_length=200) #title of post
    slug = models.SlugField(max_length=200, blank=True) #some random chars
    created_at = models.DateTimeField(auto_now_add=True) # date and time of post, by default current date&time will be set

    # post liked by which user (this can be many)
    liked_by = models.ManyToManyField(User, related_name='posts_liked', blank=True)

    def __str__(self) -> str:
        return self.title


    # overriding save method to add slug to post if slug is not set
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.SET(None), related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET(None), related_name='comment_user')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at', )

    def __str__(self):
        return f'{self.user} on {self.post.title[:30]}...'