from django.db import models
from account.models import User

class FriendRequestModel(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    requested_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ("from_user", 'to_user')

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"