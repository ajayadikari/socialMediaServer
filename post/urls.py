from django.urls import path
from .views import PostView



urlspattern = [
    path("/", PostView.as_view())
]