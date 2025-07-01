from django.urls import path
from .clubConsumer import ClubConsumer
from .personalChatConsumer import PersonalChatConsumer


urlpatterns = [
    path('club-chat/<str:club>/', ClubConsumer.as_asgi()), 
    path('personal-chat/<str:sender>/', PersonalChatConsumer.as_asgi())
]