from django.db import models
from account.models import User

# Create your models here.
class PostModel(models.Model):
    creator = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    title = models.TextField(blank=False, null=False, min=3, max_length=150)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class PostImageModel(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, null=False, blank=False, related_name="images")
    image = models.ImageField(upload_to='post/images/')

