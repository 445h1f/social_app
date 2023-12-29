from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)



# model for user profile
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user/%Y/%m/%d', default='user/blank-profile.png')


    def __str__(self) -> str:
        return str(self.user)