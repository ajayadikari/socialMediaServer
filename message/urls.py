from django.urls import path
from .views import create_message, delete_message, update_message, get_conversation


urlPatterns = [
    path('create-message/', create_message), 
    path('delete-message/', delete_message), 
    path('update-message/', update_message), 
    path('get-conversation/<str:id>', get_conversation)
]