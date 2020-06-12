from django.urls import path, include
from .views import *

app_name = 'video'

urlpatterns = [
    path('video/add_duration/', add_duration, name='add_duration'),
    path('home/', home, name='home_url'),
    path('', landing_page, name='landing_page'),
    path('video/category/', categories_list, name='categories_list'),
    path('video/detail/<int:id>/', video_detail, name='detail'),
    path('video/add/', add_video, name='add_video_url'),
    path('video/myvideo/', myvideos_list, name='myvideos_list'),

]