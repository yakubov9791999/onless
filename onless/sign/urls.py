from django.urls import path, include
from .views import *

app_name = 'sign'

urlpatterns = [
    path('', sign, name='sign'),
    path('add-schedule/', add_schedule, name='add_schedule'),
    path('add-subject/', add_subject, name='add_subject'),
    path('schedules/', schedules_list, name='schedules_list'),
    path('get-subject/', get_subject, name='get_subject'),
    path('get-schedule/', get_schedule, name='get_schedule'),

]
