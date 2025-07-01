from rest_framework.serializers import ModelSerializer
from .models import ClubClass, ClubRequestModel


class ClubSerializer(ModelSerializer):
    class Meta: 
        model = ClubClass
        fields = '__all__'
        

class ClubRequestSerializer(ModelSerializer):
    class Meta:
        model = ClubRequestModel
        fields = '__all__'