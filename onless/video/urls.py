from django.urls import path, include
from .views import *



urlpatterns = [
    path('', home),
    path('video/add_duration/', add_duration, name='add_duration'),
    path('video/mainsection/', mainsections_list, name='video_mainsections_list_url'),
    path('video/mainsection/<int:id>/', mainsection_detail, name='video_mainsection_detail_url'),
    path('video/category/', categories_list, name='video_categories_list_url'),
    path('video/category/<int:id>/', category_detail, name='video_category_detail_url'),
    path('video/detail/<int:id>/', video_detail, name='video_detail_url'),
    path('video/lesson/detail/<int:pk>/', vide_detail_view, name='vide_detail_view'),
]