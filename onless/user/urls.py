from django.urls import path, include
from .views import *



urlpatterns = [
    path('', user_login, name='login'),
    path('add/', add_list, name='add_list_url'),
    path('settings/', settings_list, name='settings_list_url'),
    path('add_teacher/', add_teacher, name='add_teacher_url'),
    path('add_pupil/', add_pupil, name='add_pupil_url'),
    path('add_group/', add_group, name='add_group_url'),
    path('groups/', groups_list, name='groups_list_url'),
    path('group/<int:id>/', group_detail, name='group_detail_url'),
    path('group_delete/<int:id>/', group_delete, name='group_delete_url'),
    path('group_update/<int:id>/', group_update, name='group_update_url'),
    path('profil_edit/', profil_edit, name='edit_profil_url'),
    path('school_edit/', school_edit, name='edit_school_url'),
    path('contact/', contact, name='contact_url'),
    path('search/', search, name='search_url'),
]
