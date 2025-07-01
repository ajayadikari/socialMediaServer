from rest_framework import serializers
from .models import ExperienceModel

def validate_job_title(self, value):
    if value is None or len(value) <= 3 or value.isalpnum() or value.isnum() == True: 
        raise Exception("Job title cannot be null and atleast have 4 characters and shouldnt be number")
    return value

class ExperienceSerializer(serializers.ModelSerializer):
    # company_name = serializers.CharField(max_length=255, allow_null=False, allow_blank=False)
    # job_title = serializers.CharField(max_length=255, required=True, allow_null=False, allow_blank=False, validators=[validate_job_title])
    # description = serializers.CharField()
    # start_date = serializers.DateField()
    # end_date = serializers.DateField()

    class Meta: 
        model = ExperienceModel
        fields = "__all__"

    def validate_company_name(self, value):
        if value is None or value == '' or len(value) <= 3:
            raise Exception('Company name cannot be null or non-string or atlease have more than 3 characters')
        return value
    
    def validate(self, validated_data): 
        if validated_data.get('start_date', None) is not None and validated_data.get('end_date', None) is not None:
            if(validated_data.get('start_date', None) > validated_data.get('end_date', None)):
                raise Exception('Start date can never be greater than end date')
        return validated_data
    
    
    def create(self, validated_data):
        return ExperienceModel.objects.create(**validated_data)
    
    def update(self, instance, validate_data):
        instance.company_name = validate_data.get('company_name', instance.company_name)
        instance.job_title = validate_data.get('job_title', instance.job_title)
        instance.description = validate_data.get('description', instance.description)
        instance.start_date = validate_data.get('start_date', instance.start_date)
        instance.end_date = validate_data.get('start_date', instance.end_date)

        instance.save()
        return instance
        