from django.urls import path, include
from .views import *



urlpatterns = [
    path('', home),
    path('video/add_duration/', add_duration, name='add_duration'),
    path('video/lessons/', video_lessons, name='video_lessons'),
]