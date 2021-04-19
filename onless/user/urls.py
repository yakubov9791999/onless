from django.urls import path, include
from .views import *

app_name = 'user'

urlpatterns = [
    path('', user_login, name='login'),
    path('add/', add_list, name='add_list'),
    path('settings/', settings_list, name='settings_list'),
    path('worker-add/', worker_add, name='worker_add'),
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
    path('bugalter/groups/', bugalter_groups_list, name='bugalter_groups_list'),
    path('bugalter/group/<int:id>/', bugalter_group_detail, name='bugalter_group_detail'),
    path('set-pay/', set_pay, name='set_pay'),
    path('remove-pay/<int:id>/', remove_pay, name='remove_pay'),
    path('pay-history/<int:user_id>/<int:group_id>/', pay_history, name='pay_history'),
    path('history/view-video/all/', history_view_video_all, name='history_view_video_all'),
    path('history/pupil-view-video/<int:id>/', history_pupil_view_video, name='history_pupil_view_video'),
    path('get-district/', get_district, name='get_district'),
    path('getDistrict/', getDistrict, name='getDistrict'),

    path('school-groups/<int:id>/', school_groups, name='school_groups'),
    path('school-group/<int:id>/', school_group_detail, name='school_group_detail'),
    path('support/', support, name='support'),
    path('result/<int:id>/', result, name='result'),
    path('xabarlar/', messeges, name='messeges'),
    path('get-learning-type/', get_learning_type, name='get_learning_type'),

    path('attendance-groups-list/', attendance_groups_list, name='attendance_groups_list'),

    path('attendance-set-by-group/<int:id>/', attendance_set_by_group, name='attendance_set_by_group'),
    path('attendance-set-by-subject/<int:group_id>/<int:subject_id>/', attendance_set_by_subject,
         name='attendance_set_by_subject'),
    path('attendance-set-visited/', attendance_set_visited, name='attendance_set_visited'),
    path('send-sms/', send_sms, name='send_sms'),

    path('referral-list/<int:id>/', referral_list, name='referral_list'),

    path('rating-groups-list/', rating_groups_list, name='rating_groups_list'),
    path('rating-set-by-group/<int:id>/', rating_set_by_group, name='rating_set_by_group'),
    path('rating-set-by-subject/<int:group_id>/<int:subject_id>/', rating_set_by_subject, name='rating_set_by_subject'),
    path('electronical-journal/', electronical_journal, name='electronical_journal'),
    path('rating-create/', rating_create, name='rating_create'),
    path('get-group-pupils-count/', get_group_pupils_count, name='get_group_pupils_count'),
    path('get-workers-count/', get_workers_count, name='get_workers_count'),
    # path('get-attendance-time/', get_attendance_time, name='get_attendance_time'),
    path('get-group-months/', get_group_months, name='get_group_months'),
    path('sms-settings/', sms_settings, name='sms_settings'),

    path('modify-checkbox-send-sms/', modify_checkbox_send_sms, name='modify_checkbox_send_sms'),
    path('payment-payme/', payment_payme, name='payment_payme'),
    path('personal-exam-doc-generate/<int:id>/', personal_exam_doc_generate, name='personal_exam_doc_generate'),

]
