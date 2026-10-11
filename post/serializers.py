from rest_framework import serializers
from PIL import Image, UnidentifiedImageError
from .models import PostModel, PostImageModel, PostFileModel


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImageModel
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "post": {"read_only": True},
        }

    def validate_image(self, image_file):
        if image_file.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "Image size cannot exceed 5 MB."
            )

        image = Image.open(image_file)

        if image.format not in ("PNG", "JPEG", "WEBP"):
            raise serializers.ValidationError(
                "Allowed formats: PNG, JPEG, WEBP."
            )

        if image.width > 600 or image.height > 450:
            raise serializers.ValidationError(
                "Maximum dimensions: 600 × 450 pixels."
            )
        return image_file


class PostFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFileModel
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "post": {"read_only": True},
        }

    def validate_file(self, file):
        if file.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "File size cannot exceed 5 MB."
            )

        allowed_extensions = (".pdf", ".doc", ".docx")

        if not file.name.lower().endswith(allowed_extensions):
            raise serializers.ValidationError(
                "Only PDF, DOC, and DOCX files are allowed."
            )

        return file

class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, required=False)
    files = PostFileSerializer(many=True, required=False)

    class Meta:
        model = PostModel
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def validate(self, attrs):
        title = attrs.get("title")

        if title is not None and not 3 <= len(title) <= 150:
            raise serializers.ValidationError({
                "title": "Title must be between 3 and 150 characters."
            })

        return attrs

    def create(self, validated_data):
        images = validated_data.pop("images", [])
        files = validated_data.pop("files", [])

        post = PostModel.objects.create(**validated_data)

        for image_data in images:
            PostImageModel.objects.create(
                post=post,
                **image_data
            )

        for file_data in files:
            PostFileModel.objects.create(
                post=post,
                **file_data
            )

        return post

    def update(self, instance, validated_data):
        images = validated_data.pop("images", [])
        files = validated_data.pop("files", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        for image_data in images:
            PostImageModel.objects.create(
                post=instance,
                **image_data
            )

        for file_data in files:
            PostFileModel.objects.create(
                post=instance,
                **file_data
            )

        return instance