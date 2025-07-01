from django.urls import path
from .views import accept_friend_request, get_friend_requests, get_my_reqests, send_friend_request, reject_friend_request

urlpatterns = [
    path('accept-friend-request/<str:requestedUserId>/', accept_friend_request), 
    path('get-friend-requests/', get_friend_requests), 
    path('get-my-requests/', get_my_reqests), 
    path('send-friend-request/<str:id>/', send_friend_request), 
    path('reject-friend-request/<str:requestedUserId>/', reject_friend_request)
]