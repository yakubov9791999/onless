from django.urls import path, include
from .views import *



urlpatterns = [
    path('', user_login, name='login'),
    path('add/', add_list, name='add_list_url'),
    path('add_teacher/', add_teacher, name='add_teacher_url'),
    path('add_pupil/', add_pupil, name='add_pupil_url'),
    path('add_group/', add_group, name='add_group_url'),
    path('groups/', groups_list, name='groups_list_url'),
    path('group/<int:id>/', group_detail, name='group_detail_url'),
]
