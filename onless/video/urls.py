from django.urls import path, include
from .views import *



urlpatterns = [
    path('video/add_duration/', add_duration, name='add_duration'),
    path('mainsections/', mainsections_list, name='video_mainsections_list_url'),
    path('home/', home, name='home_url'),
    path('', landing_page, name='landing_page__url'),
    path('video/mainsection/<int:id>/', mainsection_detail, name='video_mainsection_detail_url'),
    path('video/category/', categories_list, name='video_categories_list_url'),
    path('video/category/<int:id>/', category_detail, name='video_category_detail_url'),
    path('video/detail/<int:id>/', video_detail, name='video_detail_url'),
    path('video/add/', add_video, name='add_video_url'),
    path('video/myvideo/', myvideos_list, name='myvideos_list_url'),

]