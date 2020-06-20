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
    path('pupil_edit/<int:id>/', pupil_edit, name='edit_pupil'),
    path('contact/', contact, name='contact'),
    path('search/', search, name='search'),
    path('add_school/', add_school, name='add_school'),
    path('pupil_delete/<int:id>/', pupil_delete, name='pupil_delete'),
    path('workers/', workers_list, name='workers_list'),
    path('teacher_update/<int:id>/', teacher_edit, name='teacher_edit'),
    path('teacher_delete/<int:id>/', teacher_delete, name='teacher_delete'),
    path('upload_file/', upload_file, name='upload_file'),
    path('add_bugalter/', add_bugalter, name='add_bugalter'),
    path('bugalter/groups/', bugalter_groups_list, name='bugalter_groups_list'),
    path('bugalter/group/<int:id>/', bugalter_group_detail, name='bugalter_group_detail'),
    path('add_pay/', add_pay, name='add_pay'),
    path('pay_history/<int:user_id>/<int:group_id>/', pay_history, name='pay_history'),

    path('history/view-video/all/', history_view_video_all, name='history_view_video_all'),
]
