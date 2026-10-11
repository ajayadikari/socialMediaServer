from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.permission import AllowAny, IsAuthenticated
from models import PostModel
from serializers import PostSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_SUCCESS

# Create your views here.
class PostView(APIView):



    def get_permission(self, req):
        if req.method == 'get':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self):
        posts_qs = PostModel.objects.all()

        posts = PostSerializer(posts_qs, many=True)

        return Response({
            "success": True,
            "message": "posts fetched successfully",
            "data": posts.data
        }, status=HTTP_200_SUCCESS)


    def post(self, req):
        try:
            user = req.user
            if user is None:
                return Response({
                    "success": False,
                    "message": "please logout and login!"
                })
            data = req.data
            post = PostSerializer(**data)

            if post.is_valid():
                post.save()
                return Response ({
                    "success": True,
                    "message": "post saved",
                    "data": post
                }, status=HTTP_200_SUCCESS)

            return Response({
                "success": False, 
                "message": "post save failed due to validation error",
                "errors": post.validation_errors
            })

        except Exception as err:
            print(str(err))
            return Response({
                "success": False, 
                "message": "failed to save post",
                "error": err
            })


        

        

        