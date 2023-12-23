from django.db import models
from django.conf import settings

# Create your models here.

# model for user profile
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user/%Y/%m/%d', default='no_profile.png')


    def __str__(self) -> str:
        return str(self.user)