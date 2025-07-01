from django.db import models
from account.models import User

class ClubClass(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    image = models.ImageField(upload_to='club_images', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name="members")
    admins = models.ManyToManyField(User, related_name="admins")
    creator = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE, null=False, blank=False, default=None)


    def __str__(self):
        return self.name

    
class ClubRequestModel(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, default=None)
    club = models.ForeignKey(ClubClass, on_delete=models.CASCADE, null=False, blank=False, default=None)
