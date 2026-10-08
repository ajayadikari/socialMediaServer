from rest_framework.serializers import ModelSerializer
from models import PostModel, PostImageModel
from rest_framework.exceptions import ValidationError
from PIL import Image


class PostSerializer(ModelSerializer):
    class Meta:
        model = PostModel
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
        }


    def validate(self, obj):
        if obj.get("creator") == None:
            raise ValidationError("creator cannot be none")
        if len(obj.get("title")) < 3 or len(obj.title) > 150:
            raise ValidationError("title should have atleast 3 and max 150 characters")
        return obj


class PostImageSerializer(ModelSerializer):
    class Meta:
        model = PostImageModel
        fields = "__all__"

    def validate(self, obj):
        try:
            image_file = obj.get("image")
            if image_file is None:
                raise ValidationError("Image cannot be None")
            image = Image.open(image_file)
    
            MAX_IMAGE_FILE_SIZE = 5*1024*1024
    
            if image_file.size > MAX_IMAGE_FILE_SIZE:
                raise ValidationError("image file size cannot exceed 5mb!")
    
            ALLOWED_FORMATS = ("PNG", "JPEG", "WEBP")
    
            if image.format not in ALLOWED_FORMATS:
                raise ValidationError("allowed image format: png, jpeg, webp")
    
            MAX_WIDTH = 600
            MAX_HEIGHT = 450
    
            if image.height > MAX_HEIGHT or image.width > MAX_WIDTH:
                raise ValidationError("image can have max of 450px in height and 600px in width")

        except Exception as err:
            print(str(err))
        
        

        