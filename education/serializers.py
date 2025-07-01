from rest_framework import serializers
from .models import EducationModel
from account.models import User

class EducationSerializer(serializers.ModelSerializer):
    # institution_name = serializers.CharField(max_length=255, required=True, allow_null=False, allow_blank=False)
    # major = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    # degree = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    # start_date = serializers.DateField(required=False, allow_null=True)
    # end_date = serializers.DateField(required=False, allow_null=True)
    # cgpa = serializers.FloatField(required=False, allow_null=True)
    # user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = EducationModel
        fields = "__all__"


    def validate(self, validated_data):
        print(validated_data)
        institution_name = validated_data.get('institution_name')
        major = validated_data.get('major')

        if not institution_name or institution_name.isnumeric():
            raise Exception("Institution name cannot be empty or numeric")
        
        if major and (major.isnumeric() or major.isalnum() and not major.isalpha()):
            raise Exception("Major must contain letters and cannot be purely numeric or alphanumeric")

        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise Exception("Start date cannot be after end date")

        cgpa = validated_data.get('cgpa')
        if cgpa is not None and (cgpa < 0 or cgpa > 10):
            raise Exception("CGPA must be between 0 and 10")
        
        return validated_data

    
    def __str__(self):
        return self.institution_name
    
    def create(self, validated_data):
        return EducationModel.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.institution_name = validated_data.get('institution_name', instance.institution_name)
        instance.major = validated_data.get('major', instance.major)
        instance.degree = validated_data.get('degree', instance.degree)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.cgpa = validated_data.get('cgpa', instance.cgpa)

        instance.save()
        return instance