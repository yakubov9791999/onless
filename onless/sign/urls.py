from django.urls import path, include
from .views import *

app_name = 'sign'

urlpatterns = [
    path('', sign, name='sign'),
    path('add-schedule/', add_schedule, name='add_schedule'),
    path('update-schedule/<int:id>/', update_schedule, name='update_schedule'),
    path('delete-schedule/<int:id>/', delete_schedule, name='delete_schedule'),
    path('schedules/', schedules_list, name='schedules_list'),
    path('get-subject/', get_subject, name='get_subject'),
    path('get-schedule/', get_schedule, name='get_schedule'),

]
