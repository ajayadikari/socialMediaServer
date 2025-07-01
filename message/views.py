from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from account.models import User
from club.models import ClubClass
from .serializers import MessageSerializer
from .models import MessageClass
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_message(req):
    #implement file handling implementation
    #req.files
    try: 
        data = req.data

        sender = req.user.id
        receiverId = data.get('receiverId', None)
        clubId = data.get('clubId', None)
        if not receiverId and not clubId:
            return Response({
                "success": False, 
                "message": "Need receiverId or clubId", 
                "err": "Need receiverId or clubId"
            })
        
        receiver = None
        club = None

        msgData = {
            "sender": sender, 
            "message": data.get("message", None), 
            "image": data.get("image", None), 
            "file": data.get("file", None), 
            "club": None,
            "receiver": None
        }
        if receiverId is not None:
            receiver = User.objects.filter(id=receiverId).first()
            msgData['receiver'] = receiver.id
        else:
            club = ClubClass.objects.filter(id=clubId).first()
            msgData['club'] = club.id

        serializer = MessageSerializer(data=msgData)

        if serializer.is_valid(): 
            serializer.save()
            return Response({
                "success": True, 
                "message": "message saved!", 
                "data": serializer.data
            })
        else:
            return Response({
                "success": False, 
                "message": "message failed to be saved!", 
                "err": serializer.errors
            })

    except Exception as err:
        print("---------------------------------")
        print("error - create_message func - message/view.py")
        print(err)

        return Response({
            "success": False, 
            "message": "Error while saving message!", 
            "err": str(err)
        })
    
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_message(req):
    user = req.user
    msgId = req.data.get('messageId', None)
    if msgId is None:
        return Response({
            "success": False, 
            "message": "message id needed"
        })
    clubId = req.data.get('clubId', None)
    receiverId = req.data.get('receiverId', None)

    if not clubId and not receiverId:
        return Response({
            "success": False, 
            "message": "needed clubId or receiverId!"
        })
    message = None
    if clubId:
        club = ClubClass.objects.filter(id=clubId).first()
        if not club:
            return Response({
                "success": False, 
                "message": "club not found"
            })
        message = MessageClass.objects.filter(club=club, sender=user, id=msgId).first()
    else: 
        receiver = User.objects.filter(id=receiverId).first()
        if not receiver: 
            return Response({
                "success": False, 
                "message": "receiver not found"
            })
        message = MessageClass.objects.filter(receiver=receiver, sender=user, id=msgId).first()
    print(message)
    if not message:
        return Response({
            "success": False, 
            "message": "message not found"
        })
    
    if message.sender.id is not user.id:
        return Response({
            "success": False, 
            "message": "you can only delete your messages"
        })
    
    message.delete()

    return Response({
        "success": True, 
        "message": "message deleted"
    })


@api_view(["PUT", "PATCH"])
def update_message(req):
    return Response({
        "success": True, 
        "message": "this feature is under construction"
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_conversation(req, id):
    try:
        user = req.user
        isGroup = req.GET.get('group', False)
        if isGroup:
            # implementation pending
            pass
        friend = User.objects.filter(id=id).first()
        if friend is None:
            return Response({
                "success": False, 
                "message": "frined not found"
            })
        message_queryset = MessageClass.objects.filter(Q(sender=user.id, receiver=friend.id) | Q(sender=friend.id, receiver=user.id)).order_by('created_at')
        if message_queryset is None:
            return Response({
                "success": False, 
                "message": "start conversation"
            })
        
        serialized_messages_data = MessageSerializer(message_queryset, many=True).data

        return Response({
            "success": True, 
            "message": "fetched conversation", 
            "data": serialized_messages_data
        })
    except Exception as e:
        print("-------------------------------------")
        print("err-message-get_conversation()")
        print(e)
        return Response({
            "success": False, 
            "message": "unable to fetch conversation", 
            "err": str(e)
        })
    

    