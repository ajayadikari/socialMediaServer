from django.db import models
from account.models import User
from club.models import ClubClass

class MessageClass(models.Model):
    sender = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="receiver")
    club = models.ForeignKey(ClubClass, null=True, blank=True, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='chat_images', null=True, blank=True)
    file = models.FileField(upload_to='chat_files', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.sender.username + "|" + self.message