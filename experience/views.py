from rest_framework.decorators import api_view, permission_classes
from .serializers import ExperienceSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_experience(req):
    user = req.user
    exp_details = req.data.get('experience_details', None)
    exp_details['user'] = user.id
    
    if exp_details is not None:
        serializer = ExperienceSerializer(data=exp_details)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True, 
                "message": "Experience saved!", 
                "data": serializer.data
            })
        
        return Response({
            "success": False, 
            "message": "Error saving experience!",
            "data": serializer.data
        })