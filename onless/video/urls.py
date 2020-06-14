from django.urls import path, include
from .views import *

app_name = 'video'

urlpatterns = [
    path('video/add_duration/', add_duration, name='add_duration'),
    path('home/', home, name='home'),
    path('', landing_page, name='landing_page'),
    path('video/categories/', categories_list, name='categories_list'),
    path('video/category/<int:id>', category_detail, name='category_detail'),
    path('video/videos/<int:id>', videos_list, name='videos_list'),
    path('video/detail/<int:id>/', video_detail, name='video_detail'),
    path('video/add/', add_video, name='add_video'),
    path('video/myvideo/', myvideos_list, name='myvideos_list'),
    # path('video/categories/', show_categories,name='categories_list' )

]
