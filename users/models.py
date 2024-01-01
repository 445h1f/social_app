from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    # saving after changing username to lowercase
    def save(self, *args, **kwargs):
        self.username = self.username.lower()

        super().save(*args, **kwargs)



# model for user profile
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user/%Y/%m/%d', default='user/blank-profile.png')
    followers = models.ManyToManyField(get_user_model(), related_name='followers', blank=True)
    following = models.ManyToManyField(get_user_model(), related_name='following', blank=True)
    bio = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return str(self.user)
