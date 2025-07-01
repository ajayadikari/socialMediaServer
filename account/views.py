from .serializers import AccountSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import AccountSerializer
from experience.models import ExperienceModel
from education.models import EducationModel
from experience.serializers import ExperienceSerializer
from education.serializers import EducationSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(req):

    details = req.data
    serializer = AccountSerializer(data=details)
    user = None
    try: 
        if serializer.is_valid():
            user = serializer.save()
            req.user = user
            
            # create education instance
            # user can add education and experience after registeration

            # if req.data.get('education', None) is not None:
            #     edu_res = create_education(req)

            #     if edu_res.get('success') is False:
            #         setattr(edu_res, 'message', 'User Created, error in creating education')
            #         return edu_res
            
            # if req.data.get('experience', None) is not None:
            #     exp_res = create_experience(req)

            #     if exp_res.get('success') is False:
            #         setattr(exp_res, 'message', 'user and edcation created, error in creating experience')

            return Response({
                "success": True, 
                "message": "User Creation Successful!", 
                "user": serializer.data
            })
        else:
            print("------------------------------------------------")
            print("error occured during validating data - serializer")
            print(serializer.errors)
            return Response({
                "success": False, 
                "message": "User Creation Failed!",
                "err": serializer.errors
            })
    except Exception as err:
        print("---------------------------------------------")
        print("error while creating the user")
        print(err)
        return Response({
            "success": False, 
            "message": "User Creation Failed!",
            "err": err
        })
        


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(req):
    user = req.user
    try:
        user.delete()
        return Response({
            "success": True, 
            "message": "User Deleted"
        })
    except Exception as err: 
        print("-------------------------------------------")
        print(err)
        return Response({
            "success": False, 
            "message": "Error while deleting user", 
            "err": err
        })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(req):
    user = req.user
    data = req.data
    serializer = AccountSerializer(user, data=data, partial=True)
    if serializer.is_valid(): 
        serializer.save()
        return Response({
            "success": True, 
            "message": "Profile updated!", 
            "data": serializer.data
        })
    print("---------------------------")
    print("error - update_user - account/view")
    print(serializer.errors)
    return Response({
        "success": False, 
        "message": "Profile updation failed", 
        "err": serializer.errors
    })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(req):
    try:
        user = req.user
        user.delete()

        return Response({
            "success": True, 
            "message": "User deleted", 
        })
    except Exception as err:
        print("----------------------------------------")
        print("error deleting user")
        print(err)

        return Response({
            "success": False, 
            "message": "unable to delete user!", 
            "err": err
        })
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friends(req):
    user = req.user
    try:
        # queryset = User.objects.filter(id=user.id).first()
        # serialized_data = AccountSerializer(queryset, many=True).data
        # print(serialized_data)
        user = User.objects.filter(id=user.id).first()
        friends = user.friends.all()
        serialized_data = AccountSerializer(friends, many=True).data
        return Response({
            "success": True, 
            "message": "friends fetched",
            "friends": serialized_data
        })
    
    except Exception as err:

        print('-------------------------------')
        print('err--account--get_friends()')
        print(err)

        return Response({
            "success": False, 
            "message": "error fetching friends", 
            "err": str(err)
        })
    

@api_view(["GET"])
def get_user(req, id):
    try: 
        if not id:
            return Response({
                "success": False, 
                "message": "id needed"
            })

        user_ins = User.objects.filter(id=id).first()
        serialized_user = AccountSerializer(user_ins).data
        if serialized_user:
            return Response({
                "success": True, 
                "message": "user fetched", 
                "data": serialized_user
            })
    except Exception as e:
        print("---------------------------------------")
        print("-err-account-get_user()")
        print(e)
        return Response({
            "success": False, 
            "message": "unable to get user", 
            "err": str(e)
        })
            


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_friend(req):
    try: 
        user = req.user
        friendId = req.data.get("friendId", None)
        if friendId is None:
            return Response({
                "success": False, 
                "message": "friend id is needed!"
            })
        friend = User.objects.filter(id=friendId).first()
        
        if friend is None:
            return Response({
                "success": False, 
                "message": "user not found to make friend", 
            })
        
        user.friends.add(friend)
        user.save()

        return Response({
            "success": True, 
            "message": "friend added", 
        })
    except Exception as err:
        print("------------------------")
        print("err - add_friend - account/views")
        print(err)

        return Response({
            "success": False, 
            "message": "unable to make friend!", 
            "err": err
        })
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def remove_friend(req):
    user = req.user
    friendId = req.data.get('friendId', None)
    if friendId is None:
        return Response({
            "success": False, 
            "message": "Friend id is needed!"
        })
    friend = User.objects.filter(id=friendId).first()

    if friend is None: 
        return Response({
            "success": False, 
            "message": "Friend not found"
        })
    
    try:
        user.friends.remove(friend)
        return Response({
            "success": True, 
            "message": "friend removed", 
        })
    except Exception as err:
        print("---------------------------------------")
        print("error - remove_friend - account/views")
        print(err)
        return Response({
            "success": False,
            "message": "unable to remove the friend", 
            "err": err
        })
    

@api_view(["GET"])
def get_matching_users(req):
    try:
        query = req.query_params.get("username")
        
        if query is None or len(query) == 0:
            return Response({
                "success": False, 
                "message": "query is empty"
            })

        queryset = User.objects.filter(username__icontains=query).values("id", "username", "email", "profile_pic")
        py_data = AccountSerializer(queryset, many=True).data

        return Response({
            "success": True, 
            "message": "users fetched", 
            "users": py_data
        })
    except Exception as e:
        print("---------------------------err")
        print("error-account-get_matching_users")
        print(e)
        return Response({
            "success": False, 
            "message": "server err while fetching matching users", 
            "err": str(e)
        })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_channel_name(req, id):
    try: 
        if id is None: 
            return Response({
                "success": False, 
                "message": "user id is needed"
            })
        channel_name = User.objects.filter(id=id).values_list("channel_name")

        if channel_name is None:
            return Response({
                "success": True, 
                "message": f'no user found with id {id} or is offline'
            })
        
        return Response({
            "success": True, 
            "message": "user found", 
            "channel_name": channel_name
        })
    except Exception as e:
        print("--------------------")
        print("err--account----get_channel_name")
        print(e)
        return Response({
            "success": False, 
            "message": "error during fetching user", 
            "err": str(e)
        })
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getAllUserDetails(req, userId):
    try:
        if userId is None:
            return Response({
                "success": False, 
                "message": "user id needed"
            })
    
        curr_user = req.user

        if curr_user is None or not curr_user.is_authenticated:
            return Response({
                "success": False, 
                "message": "login required"
            })
        
        userIns = User.objects.filter(id=userId).values('id', 'username', 'first_name', 'last_name', 'email', 'profile_pic').first()

        if userIns is None:
            return Response({
                "success": False, 
                "message": "user not found"
            })
        user = AccountSerializer(userIns).data
        user_details = {
            'personal_details': user, 
        }
        
        educational_details_ins = EducationModel.objects.filter(user=curr_user)

        if educational_details_ins is not None:
            educational_details = EducationSerializer(educational_details_ins, many=True).data
            user_details['educational_details'] = str(educational_details)
        else:
            user_details['educational_details'] = None

        experience_details_ins = ExperienceModel.objects.filter(user=curr_user)

        if experience_details_ins is not None:
            experience_details = ExperienceSerializer(experience_details_ins, many=True).data
            user_details['experience_details'] = str(experience_details)
        else:
            user_details['experience_details'] = None

        return Response({
            "success": True, 
            "message": "fetched user details", 
            'user_details': user_details
        }, status=200)
    

    except Exception as err:
        print("---------------------")
        print("err---account----getalluserdetails()")
        print(err)
        return Response({
            "success": False, 
            "message": "internal server error", 
            "err": str(err)
        })



