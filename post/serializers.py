from rest_framework.serializers import ModelSerialisers
from models import PostModel, PostImageModel


class PostSerializers(ModelSerialisers):
    class Meta:
        model = PostModel
        fields = "__all__"
        extra_kwargs = {
            "creator": {"read_only": True},
            "id": {"read_only": True},
            "creator": {"read_only":True}
        }


    def validate(self, obj):
        if obj.creator == None:
            raise ValidationError("creator cannot be none")
        if len(obj.title) < 3 or len(obj.title) > 150:
            raise ValidationError("title should have atleast 3 and max 150 characters")
        return obj
        