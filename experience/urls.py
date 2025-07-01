from django.urls import path
from .views import create_experience


urlpattern = [
    path('create-experience/', create_experience)
]