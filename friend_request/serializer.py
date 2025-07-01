from rest_framework import serializers
from .models import FriendRequestModel


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequestModel
        fields=['from_user', 'to_user', 'requested_at']