from rest_framework.serializers import ModelSerializer
from .models import User


class AccountSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_pic', 'friends', 'channel_name']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    #write field validation function for image, for size checking, format checking, etc

    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     user = User(**validated_data)
    #     user.set_password(password)
    #     user.save()
    #     return user
    
    # def update(self, instance, validated_data):
    #     password = validated_data.pop('password', None)
    #     for attr, val in validated_data.items():
    #         setattr(instance, attr, val)
    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance
        
