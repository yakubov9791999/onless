from django.urls import path, include
from .views import *



urlpatterns = [
    path('add_duration/', add_duration, name='add_duration'),
    path('', mainsections_list, name='video_mainsections_list_url'),
    path('mainsection/<int:id>/', mainsection_detail, name='video_mainsection_detail_url'),
    path('category/', categories_list, name='video_categories_list_url'),
    path('category/<int:id>/', category_detail, name='video_category_detail_url'),
    path('detail/<int:id>/', video_detail, name='video_detail_url'),

]