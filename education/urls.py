from django.urls import path
from .views import create_education


urlpatterns = [
    path('create-education/', create_education)
]