from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import EducationSerializer
from rest_framework.permissions import IsAuthenticated
from account.models import User



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_education(req):
    user = req.user
    edu_details = req.data.get('education', None)
    if edu_details is None:
        raise Exception('No education details found')
    edu_details["user"] = user.id
    serializer = EducationSerializer(data=edu_details)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "success": True,
            "message": "Details saved!",
            "data": serializer.data
        })
    return Response({
        "success": False, 
        "message": "Server error while saving data!", 
        "err": serializer.errors
    })
    
