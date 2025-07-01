from rest_framework.serializers import ModelSerializer
from .models import MessageClass



class MessageSerializer(ModelSerializer):
    class Meta:
        model = MessageClass
        fields = '__all__'

    
    def validate(self, validated_data):
        print(validated_data)
        if(validated_data.get('receiver', None) is None and validated_data.get('club', None) is None):
            raise Exception("Receiver and club cannot be none at once!")
        if(validated_data.get('message', None) is None and validated_data.get('image', None) is None and validated_data.get('file', None) is None):
            raise Exception("no text message, image or file is found to save!")
        
        return validated_data