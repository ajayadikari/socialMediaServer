from django.apps import apps
from asgiref.sync import sync_to_async
import traceback

@sync_to_async
def add_channel_name_to_user(user_id, channel_name):
    try:
        User = apps.get_model('account', 'User')
        user = User.objects.filter(id=user_id).first()
        if user:
            user.channel_name = channel_name
            user.save()
        else:
            print(f"User with ID {user_id} not found.")
    except Exception as e:
        print("Error while updating channel name:")
        traceback.print_exc()
        raise Exception("Error while updating channel name")


@sync_to_async
def set_channel_name_to_null(channel_name):
    try:
        User = apps.get_model("account", "User")
        user = User.objects.filter(channel_name=channel_name).first()
        if(user):
            user.channel_name = None;
        else:
            print(f"User with channel name {channel_name} not found.")
    except Exception as err:
        print(str(err))

@sync_to_async
def get_user_channel_name(reveiverId):
    try:
        User = apps.get_model("account", "User")
        receiver = User.objects.filter(id=reveiverId).first()
        return receiver.channel_name
    except Exception as err:
        print(err)
        return None
