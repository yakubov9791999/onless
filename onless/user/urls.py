from django.urls import path, include
from .views import *

app_name = 'user'

urlpatterns = [
    path('', user_login, name='login'),
    path('add/', add_list, name='add_list'),
    path('settings/', settings_list, name='settings_list'),
    path('add-teacher/', add_teacher, name='add_teacher'),
    path('add-pupil/', add_pupil, name='add_pupil'),
    path('add-group/', add_group, name='add_group'),
    path('groups/', groups_list, name='groups_list'),
    path('group/<int:id>/', group_detail, name='group_detail'),
    path('group-delete/<int:id>/', group_delete, name='group_delete'),
    path('group-update/<int:id>/', group_update, name='group_update'),
    path('profil-edit/', profil_edit, name='edit_profil'),
    path('school-edit/', school_edit, name='edit_school'),
    path('pupil-edit/<int:id>/', pupil_edit, name='edit_pupil'),
    path('contact/', contact, name='contact'),
    path('search/', search, name='search'),
    path('pupil-delete/<int:id>/', pupil_delete, name='pupil_delete'),
    path('workers/', workers_list, name='workers_list'),
    path('worker-update/<int:id>/', worker_edit, name='worker_edit'),
    path('worker-delete/<int:id>/', worker_delete, name='worker_delete'),
    path('upload-file/', upload_file, name='upload_file'),
    path('add-bugalter/', add_bugalter, name='add_bugalter'),
    path('bugalter/groups/', bugalter_groups_list, name='bugalter_groups_list'),
    path('bugalter/group/<int:id>/', bugalter_group_detail, name='bugalter_group_detail'),
    path('add-pay/', add_pay, name='add_pay'),
    path('pay-history/<int:user_id>/<int:group_id>/', pay_history, name='pay_history'),
    path('history/view-video/all/', history_view_video_all, name='history_view_video_all'),
    path('history/pupil-view-video/<int:id>/', history_pupil_view_video, name='history_pupil_view_video'),
    path('get-district/', get_district, name='get_district'),
    path('school-groups/<int:id>/', school_groups, name='school_groups'),
    path('school-group/<int:id>/', school_group_detail, name='school_group_detail'),
    path('messeges/', messeges, name='messeges'),

]

