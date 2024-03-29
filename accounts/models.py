from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_image/', null=True, blank=True)
    nickname = models.CharField(max_length=8, default='무지')
    exp = models.IntegerField(default=100)
