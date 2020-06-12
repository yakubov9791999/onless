from django.urls import path, include
from .views import *

app_name = 'user'

urlpatterns = [
    path('', user_login, name='login'),
    path('add/', add_list, name='add_list'),
    path('settings/', settings_list, name='settings_list'),
    path('add_teacher/', add_teacher, name='add_teacher'),
    path('add_pupil/', add_pupil, name='add_pupil'),
    path('add_group/', add_group, name='add_group'),
    path('groups/', groups_list, name='groups_list'),
    path('group/<int:id>/', group_detail, name='group_detail'),
    path('group_delete/<int:id>/', group_delete, name='group_delete'),
    path('group_update/<int:id>/', group_update, name='group_update'),
    path('profil_edit/', profil_edit, name='edit_profil'),
    path('school_edit/', school_edit, name='edit_school'),
    path('contact/', contact, name='contact'),
    path('search/', search, name='search'),
    path('add_school/', add_school, name='add_school'),
    path('schools/', schools_list, name='schools_list'),
]
