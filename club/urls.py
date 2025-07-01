from django.urls import path
from .views import add_member, create_club, delete_club, exit_club, get_user_clubs, make_admin, remove_admin_status, remove_member, update_club, get_matching_clubs, request_club, reject_request, accept_request, get_joining_requests, get_club_members


urlPatterns = [
    path('add-member/', add_member),
    path('create-club/', create_club),
    path('delete-club/', delete_club),
    path('exit-club/', exit_club), 
    path('get-user-clubs/', get_user_clubs),
    path('make-admin/', make_admin), 
    path('remove-admin-status/', remove_admin_status),
    path('remove-member/', remove_member),
    path('update-club/', update_club), 
    path('get-matching-clubs/', get_matching_clubs), 
    path('get-joining-requests/<str:clubId>', get_joining_requests),
    path('send-join-request/<str:clubId>/', request_club), 
    path('accept-request/<str:reqId>/', accept_request), 
    path('reject-request/<str:reqId>/', reject_request), 
    path('get-club-members/<str:clubId>', get_club_members),
]