from django.urls import path, include
from .views import *

app_name = 'sign'

urlpatterns = [
    path("belgilar/", sign, name='sign'),
    # path('add-subject/', add_subject, name='add_subject'),
    path('update-schedule/<int:id>/', update_schedule, name='update_schedule'),
    # path('update-subject/<int:id>/', update_subject, name='update_subject'),
    path('delete-schedule/<int:id>/', delete_schedule, name='delete_schedule'),
    path('schedules/', schedules_list, name='schedules_list'),
    path('save-schedule/', save_schedule, name='save_schedule'),
    path('subjects/', subjects_list, name='subjects_list'),
    path('get-subject/', get_subject, name='get_subject'),
    path('get-subject-long-title/', get_subject_long_title, name='get_subject_long_title'),

    path('group-subjects/', group_subjects, name='group_subjects'),
    path('get-schedule/', get_schedule, name='get_schedule'),
    path('materials/', materials, name='materials'),
    path('add-material/', add_material, name='add_material'),
    path('get-video/', get_video, name='get_video'),
    path('delete-material/<int:id>/', delete_material, name='delete_material'),
    # path("traffic_rules/", traffic_rules, name='traffic_rules'),

]
