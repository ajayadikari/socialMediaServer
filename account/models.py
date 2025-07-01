from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .manager import UserManager

class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False, null=False)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)
    channel_name = models.TextField(unique=True, null=True, blank=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 
    