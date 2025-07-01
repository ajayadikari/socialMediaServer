from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ClubSerializer, ClubRequestSerializer
from .models import ClubClass, ClubRequestModel
from account.models import User
from rest_framework.permissions import IsAuthenticated



# implement model permissions like has perms for below views
#----------------------------------------------------------------


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_club(req):
    try:
        creator = req.user
        data = req.data.copy()
        data['creator'] = creator.id
        data.setlist('members', [str(creator.id)])
        data.setlist('admins', [str(creator.id)])

        name = data.get('name')

        club = ClubClass.objects.filter(name=name).first()

        if club is not None:
            return Response({
                "success": False, 
                "message": "club name is in use"
            })
        
        serializer_data = ClubSerializer(data=data)
        if serializer_data.is_valid():
            saved_data = serializer_data.save()

            return Response({
                "success": True, 
                "message": "club creation successful", 
                "data": str(saved_data)
            })
        return Response({
            "success": False, 
            "message": "errors during creating club!", 
            "err": str(serializer_data.errors)
        })
    except Exception as err:
        print("------------------------------")
        print("error - create_club - club/views")
        print(err)
        return Response({
            "success": False, 
            "message": "unable to create club", 
            "err": str(err)
        })
    
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_club(req):
    user = req.user
    clubId = req.data.get('clubId')
    if clubId is None:
        return Response({
            "success": False, 
            "message": "club id needed"
        })
    club = ClubClass.objects.filter(id=clubId).first()
    if club is None:
        return Response({
            "success": False, 
            "message": "club not found"
        })
    creator = club.creator
    if user.id is not creator.id:
        return Response({
            "success": False, 
            "message": "only creator can be the destroyer"
        })
    
    club.delete()

    return Response({
        "success": True, 
        "message": "club deleted", 
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_club(req):
    user = req.user
    data = req.data
    clubId = data.get('clubId', None)

    if clubId is None:
        return Response({
            "success": False, 
            "message": "club id is needed"
        })
    
    club = ClubClass.objects.filter(id=clubId).first()

    if club is None:
        return Response({
            "success": False, 
            "message": "club not found"
        })
    
    if club.admins.contains(user):
        try:
            serializer = ClubSerializer(club, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True, 
                    "message": "club updated", 
                    "data": str(serializer.data)
                })
        except Exception as err:
            print("------------------------------------")
            print("error - update_club - club/views")
            print(err)
            return Response({
                "success": False, 
                "message": "club updation failed", 
                "err": str(err)
            })
    
    return Response({
        "success": False, 
        "message": "Only admins can update club"
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAuthenticated])
def get_user_clubs(req):
    try:

        user = req.user

        user_clubs = ClubClass.objects.filter(members=user).prefetch_related('members')

        serializer = ClubSerializer(user_clubs, many=True)

        return Response({
            "success": True, 
            "message": "user clubs fetched", 
            "clubs": serializer.data
        })
    
    except Exception as err:
        print("-----------------------------------------")
        print("error - get_user_club - club/views")
        print(err)
        return Response({
            "success": False, 
            "message": "unable fetch user clubs", 
            "err": err
        })
    
@api_view(["PUT", "PATCH"])
def exit_club(req):
    user = req.user
    clubId = req.data.get("clubId", None)
    if clubId is None:
        return Response({
            "success": False, 
            "message": "club id is needed!"
        })
    
    club = ClubClass.objects.filter(id=clubId).first()

    if club is None:
        return Response({
            "success": False, 
            "message": "club not found!"
        })
    
    try:
        club.members.remove(user)
        club.admins.remove(user)

        return Response({
            "success": True, 
            "message": "club exited"
        })
    
    except Exception as err:
        print("----------------------------------------")
        print("error - exit_club - club/views")
        print(err)
        return Response({
            "success": False, 
            "message": "error existing club", 
            "err": err
        })
    


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_club_members(req, clubId):
    try:
        user = req.user
        if not user and not user.is_authenticated:
            return Response({
                "success": False, 
                "message": "please login"
            })
        
        
        
        queryset = ClubClass.objects.filter(id=clubId).prefetch_related('members').first()
        if not queryset:
            return Response({
                "success": False, 
                "message": "club not found"
            })
        
        member = queryset.members.filter(id=user.id)

        if not member.exists():
            return Response({
                "success": False, 
                "message": "only members and admins of the club can access members"
            })
        
        members = []

        for member in queryset.members.all():
            members.append({
                "id": member.id, 
                "username": member.username, 
                "profile_pic": member.profile_pic.url if member.profile_pic else None
            })
        
        # serialized_data = ClubSerializer(queryset).data
        
        
        return Response({
            "success": True, 
            "message": "club members fetched", 
            "members": members
        })


    except Exception as err:
        print("-----------------------")
        print("club--get_club_members()")
        print(err)
        return Response({
            "success": False, 
            "message": "internal server error", 
            "err": str(err)
        })
    

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def add_member(req):
    try:
        clubId = req.data.get('clubId', None)
        if clubId is None:
            return Response({
                "success": False, 
                "message": "club id is needed!"
            })
        club = ClubClass.objects.filter(id=clubId).first()
        if club is None:
            return Response({
                "success": False, 
                "message": "clud not found"
            })
        
        user = req.user
        memberId = req.data.get('memberId', None)
        if memberId is None:
            return Response({
                "success": False, 
                "message": "memberId is needed"
            })
        
        member = User.objects.filter(id=memberId).first()
        if member is None:
            return Response({
                "success": False, 
                "message": "user not be added"
            })
        if club.admins.contains(user):

            if club.members.filter(id=member.id).exists():
                return Response({
                    "success": False, 
                    "message": "already a member"
                })
            
            club.members.add(member)

            return Response({
                "success": True, 
                "message": "member added",
                "members": list(club.members.values('id', 'username'))
            })
        else:
            return Response({
                "success": False, 
                "message": "only admin can added members!"
            })
        
    except Exception as err:
        print("-------------------------------")
        print("error - add_member - club/views")
        print(err)
        
        return Response({
            "success": False, 
            "message": "unable to add the member", 
            "err": str(err)
        })
    
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def remove_member(req):
    try: 
        user = req.user
        clubId = req.data.get('clubId', None)
        if clubId is None:
            return Response({
                "success": False, 
                "message": "club id is needed"
            })
        
        club = ClubClass.objects.filter(id=clubId).first()
        
        if club is None:
            return Response({
                "success": False, 
                "message": "club not found"
            })
        
        memberId = req.data.get('memberId', None)
        if memberId is None:
            return Response({
                "success": False, 
                "message": "member id is needed"
            })
        member = User.objects.filter(id=memberId).first()
        if not club.members.filter(id=memberId).exists():
            return Response({
                "success": False, 
                "message": "cannot remove a non-member of club"
            })
        
        if not club.admins.filter(id=user.id).exists():
            return Response({
                "success": False, 
                "message": "only admins can remove members"
            })
        
        club.members.remove(member)

        return Response({
            "success": True, 
            "message": "member removed", 
            "members": list(club.members.values('id', 'username'))
        })
    except Exception as err:
        
        print("-----------------------------------------")
        print("error - remove_member - club/views")
        print(err)

        return Response({
            "success": False, 
            "message": "error removing member", 
            "err": str(err)
        })
    
    
# implement ban_member
#----------------------

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def make_admin(req):
    try:
        clubId = req.data.get('clubId', None)
        if clubId is None:
            return Response({
                "success": False, 
                "message": "needed clubId"
            })
        club = ClubClass.objects.filter(id=clubId).first()
        if club is None:
            return Response({
                "success": False, 
                "message": "club not found"
            })
        user = req.user
        if not club.admins.filter(id=user.id).exists():
            return Response({
                "success": False, 
                "message": "only admin can make admins"
            })
        memberId = req.data.get('memberId', None)
        if memberId is None:
            return Response({
                "success": False, 
                "message": "needed memberId"
            })
        
        member = User.objects.filter(id=memberId).first()

        if member is None:
            return Response({
                "success": False, 
                "message": "user not found!"
            })
        
        if club.admins.filter(id=member.id).exists():
            return Response({
                "success": False, 
                "message": "Already a Admin"
            })
        
        if not club.members.filter(id=member.id).exists():
            return Response({
                "success": False, 
                "message": f"{member.username} is not member of this club"
            })
        
        club.admins.add(member)

        return Response({
            "success": True, 
            "message": f"{member.username} became admin"
        })
    
    except Exception as err:

        print("---------------------------")
        print("error - make_admin - club/views")
        print(err)

        return Response({
            "success": False, 
            "message": "unable to make admin", 
            "err": str(err)
        })
    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def remove_admin_status(req):
    try: 
        clubId = req.data.get('clubId', None)
        if clubId is None: 
            return Response({
                "success": False, 
                "message": "clubId is needed"
            })
        club = ClubClass.objects.filter(id=clubId).first()
        if club is None: 
            return Response({
                "success": False, 
                "message": "club not found"
            })
        user = req.user
        if not club.admins.filter(id=user.id).exists():
            return Response({
                "success": False, 
                "message": "you are not admin"
            })
        
        adminId = req.data.get('adminId', None)

        if adminId is None:
            return Response({
                "success": False, 
                "message": "admin id is needed"
            })
        
        admin = User.objects.filter(id=adminId).first()

        if admin is None or not club.admins.filter(id=admin.id).exists():
            return Response({
                "success": False, 
                "message": "user is not admin/club member"
            })
        
        club.admins.remove(admin)

        return Response({
            "success": True, 
            "message": f"{admin.username} is no longer admin", 
        })
    except Exception as err:
        print("-----------------------------------------")
        print("error - remove_admin_status - club/views")
        print(err)

        return Response({
            "success": False, 
            "message": "unable remove admin", 
            "err": str(err)
        })
    


@api_view(['GET'])
def get_matching_clubs(req):
    try:
        query = req.query_params.get("query")
        if query is None: 
            return Response({
                "success": True, 
                "message": "needed query"
            })
        queryset = ClubClass.objects.filter(name__icontains=query).values('id', 'name', 'image')
        # clubs = ClubSerializer(queryset, many=True).data

        if not queryset.exists():
            return Response({
                "success": True, 
                "message": "no club found"
            })
        
        return Response({
            "success": True, 
            "message": "clubs fetched", 
            "clubs": queryset
        })
    except Exception as e:
        print("---------------------")
        print("err--club---get_matching_club")
        print(e)
        return Response({
            "success": True, 
            "message": "error fetching clubs", 
            "err": str(e)
        })
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_joining_requests(req, clubId):
    try:
        user = req.user
        
        if not user or not user.is_authenticated:
            return Response({
                "success": False, 
                "message": "please login"
            })
        
        club = ClubClass.objects.filter(id=clubId).first()

        if not club:
            return Response({
                "success": False, 
                "message": "club not found"
            })
        
        admin = club.admins.filter(id=user.id)

        if not admin:
            return Response({
                "success": False, 
                "message": "only admins can see requests"
            })
        
        requests_queryset = ClubRequestModel.objects.filter(club=club).select_related('requester')

        requests = []

        for req in requests_queryset:
            requests.append({
                "requestId": req.id,
                "id": req.requester.id, 
                "username": req.requester.username, 
                "profile_pic": req.requester.profile_pic if req.requester.profile_pic else None
            })

        return Response({
            "success": True, 
            "message": "joining requests fetched", 
            "requests": requests
        })

    except Exception as err:
        print("------------------------------")
        print("err--club---get_joining_requests()")
        print(err)
        return Response({
            "success": False, 
            "message": "internal server error", 
            "err": str(err)
        })
    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def accept_request(req, reqId):
    if reqId is None:
        return Response({
            "success": False, 
            "message": "requestid not found"
        })
    
    user = req.user

    if not user or not user.is_authenticated: 
        return Response({
            "success": False, 
            "message": "login required"
        })
    
    req = ClubRequestModel.objects.filter(id=reqId).first()

    if not req:
        return Response({
            "success": False, 
            "message": "request not found"
        })
    
    club = req.club
    requester = req.requester
    
    admin = club.admins.filter(id=user.id).first()

    if not admin:
        return Response({
            "success": False, 
            "message": "only admins allowed"
        })
    
    member = club.members.filter(id=requester.id).first()

    if member:
        return Response({
            "success": False, 
            "message": "already a member"
        })
    
    club.members.add(requester)

    req.delete()

    return Response({
        "success": True, 
        "message": "request accepted"
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def reject_request(req, reqId):

    if reqId is None:
        return Response({
            "success": False, 
            "message": "request id is needed"
        })
    
    user = req.user

    if not user or not user.is_authenticated:
        return Response({
            "success": False, 
            "message": "login required"
        })
    
    req = ClubRequestModel.objects.filter(id=reqId).first()

    if not req:
        return Response({
            "success": False, 
            "message": "request not found"
        })
    
    club = req.club

    admin = club.admins.filter(id=user.id)

    if not admin:
        return Response({
            "success": False, 
            "message": "only admins can reject request"
        })
    
    req.delete()

    return Response({
        "success": True, 
        "message": "request rejected"
    })

    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_club(req, clubId):

    try:
        requester = req.user

        if requester is None:
            return Response({
                "success": False, 
                "message": "please login to send joining request to club"
            })

        if clubId is None:
            return Response({
                "success": False, 
                "message": "club id needed"
            })
        
        club = ClubClass.objects.filter(id=clubId).first()

        if club is None:
            return Response({
                "success": False, 
                "message": "club not found"
            })
        
        req = ClubRequestModel.objects.filter(requester=requester, club=club).first()

        if req:
            return Response({
                "success": False, 
                "message": "you requested already"
            })
        
        ClubRequestModel.objects.create(requester=requester, club = club)
        
        return Response({
            "success": True, 
            "message": "request sent",
        })
    except Exception as err:
        print("-------------------------")
        print("club--request_club()")
        print(err)

        return Response({
            "success": False, 
            "message": "internal server error", 
            "err": str(err)
        })

    


    