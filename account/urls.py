from django.urls import path
from .views import signup, delete_user, add_friend, get_friends, remove_friend, update_user, get_channel_name, get_matching_users, get_user, getAllUserDetails

urlpattern = [
    path('signup/', signup),
    path('delete-user/', delete_user), 
    path('update-user/', update_user), 
    path('get-friends/', get_friends),
    path('add-friend/', add_friend),
    path('remove-friend/', remove_friend),
    path('get-matching-user/', get_matching_users), 
    path('get-channel-name/<str:id>/', get_channel_name),
    path('get-user/<str:id>/', get_user),
    path('get-all-user-details/<str:userId>/', getAllUserDetails),
]