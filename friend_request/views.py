from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import FriendRequestModel
from .serializer import FriendRequestSerializer
from rest_framework.response import Response
from account.models import User
from account.serializers import AccountSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_friend_requests(req):
    try:
        user = req.user
        queryset = FriendRequestModel.objects.filter(to_user=user).select_related('from_user')
        serialized_data = FriendRequestSerializer(queryset, many=True).data
        data = []
        for obj in serialized_data:
            user = {}
            userId = obj.get('from_user')
            user_ins = User.objects.filter(id=userId).values('id', 'username', 'email', 'profile_pic').first()
            if user_ins is None:
                continue
            serialized_user = AccountSerializer(user_ins).data
            data.append(serialized_user)
        return Response({
            "success": True, 
            "message": "fetched users sent you request", 
            "data": data
        })
    except Exception as e:
        print("-------------------------------")
        print("err--freind_request---get_friend_requests")
        print(str(e))
        return Response({
            "success": False, 
            "message": "error fetching friend requests", 
            "err": str(e)
        })
        


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_friend_request(req, id):
    try:
        from_user = req.user
        to_user = User.objects.filter(id=id).first()
        if from_user == to_user:
            return Response({
                "success": False, 
                "message": "cannot friend request yourself"
            })
        if not from_user or not to_user:
            return Response({
                "success": False, 
                "message": "missing from_user and to_user id"
            })
        req = FriendRequestModel.objects.filter(from_user=from_user, to_user=to_user).first()
        if req is not None:
            return Response({
                "success": False, 
                "message": "you already sent request"
            })
        FriendRequestModel.objects.create(from_user=from_user, to_user=to_user)
        return Response({
            "success": True, 
            "message": "friend request sent"
        })
    except Exception as e:
        print("--------------------------------")
        print("err--friend_request(module)--friend_requests")
        print(str(e))
        return Response({
            "success": False, 
            "message": "friend request failed", 
            "err": str(e)
        })
    

# need to test this api
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_reqests(req):
    try:
        user = req.user
        if not user:
            return Response({
                "success": False, 
                "message": "login required"
            })
        queryset = FriendRequestModel.objects.filter(from_user=user)
        serialized_data = FriendRequestSerializer(data=queryset).data
        return Response({
            "success": True, 
            "message": "fetched your requests", 
            "data": serialized_data
        })
    except Exception as e:
        print("------------------------")
        print("err--friend_request(module)---get_my_requests()")
        print(str(e))

        return Response({
            "success": False, 
            "message": "requests fetching failed", 
            "err": str(e)
        })



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, requestedUserId):
    try:
        user = request.user
        requestedUser = User.objects.filter(id=requestedUserId).first()

        req = FriendRequestModel.objects.filter(from_user=requestedUser, to_user=user).first()

        if user == requestedUser:
            req.delete()
            return Response({
                "success": False, 
                "message": "cannot be friend yourself"
            })

        if not req:
            return Response({
                "success": False, 
                "message": "he didn't made a friend request"
            })

        if requestedUser is None:
            return Response({
                "success": False, 
                "message": "user not found to accept request"
            })
        
        if user.friends.contains(requestedUser):
            req.delete()
            return Response({
                "success": False, 
                "message": "already friends"
            })
        
        user.friends.add(requestedUserId)
        user.save()

        req.delete()

        return Response({
            "success": True, 
            "message": "you both are friends now"
        })
    
    except Exception as e:
        print("---------------------------")
        print('err--friend_request(module)---accept_friend_request')
        print(str(e))
        return Response({
            "success": False,
            "message": "unable make friend", 
            "err": str(e)
        })


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def reject_friend_request(req, requestedUserId):
    try:
        user = req.user
        requested_user = User.objects.filter(id=requestedUserId)
        if not user or not requested_user:
            return Response({
                "success": False, 
                "message": "user not found"
            })
        req = FriendRequestModel.objects.filter(from_user=requested_user, to_user=user).first()
        
        if req is None:
            return Response({
                "success": False, 
                "message": "he never sent you friend request"
            })
        
        req.delete()

        return Response({
            "success": True, 
            "message": "request rejected"
        })
    
    except Exception as e:
        print("--------------------------------")
        print("err--friend_request(module)--reject_friend-request()")
        print(e)

        return Response({
            "success": False, 
            "message": "unable to reject friend request", 
            "err": str(e)
        })
    
