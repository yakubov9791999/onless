from django.urls import path, include
from .views import *

app_name = 'sign'

urlpatterns = [
    path("belgilar/", sign, name='sign'),
    path('add-schedule/', add_schedule, name='add_schedule'),
    path('update-schedule/<int:id>/', update_schedule, name='update_schedule'),
    path('delete-schedule/<int:id>/', delete_schedule, name='delete_schedule'),
    path('schedules/', schedules_list, name='schedules_list'),
    path('subjects/', subjects_list, name='subjects_list'),
    path('get-subject/', get_subject, name='get_subject'),
    path('get-schedule/', get_schedule, name='get_schedule'),
    path('materials/', materials, name='materials'),
    path('add_material/', add_material, name='add_material'),
    path('get-video/', get_video, name='get_video'),
    path('delete-material/<int:id>/', delete_material, name='delete_material'),

]
