from django.urls import path
from clinet import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.dashboard_login, name="login"),
    path('logout/', views.dashboard_logout, name="logout"),

    path('carmodel_list/', views.carmodel_list, name="carmodel_list"),
    path('carmodel_create/', views.carmodel_create, name="carmodel_create"),
    path('<int:pk>carmodel_edit/', views.carmodel_edit, name="carmodel_edit"),
    path('<int:pk>/carmodel_delete/', views.carmodel_delete, name="carmodel_delete"),

    path('car_list/', views.car_list, name="car_list"),
    path('car_create/', views.car_create, name="car_create"),
    path('<int:pk>car_edit/', views.car_edit, name="car_edit"),
    path('<int:pk>/car_delete/', views.car_delete, name="car_delete"),

    path('practical_list/', views.practical_list, name="practical_list"),
    path('practical_create/', views.practical_create, name="practical_create"),
    path('<int:pk>practical_edit/', views.practical_edit, name="practical_edit"),
    path('<int:pk>/practical_delete/', views.practical_delete, name="practical_delete"),

    path('paymentforpractical_list/', views.paymentforpractical_list, name="paymentforpractical_list"),
    path('paymentforpractical_create/', views.paymentforpractical_create, name="paymentforpractical_create"),
    path('<int:pk>paymentforpractical_edit/', views.paymentforpractical_edit, name="paymentforpractical_edit"),
    path('<int:pk>/paymentforpractical_delete/', views.paymentforpractical_delete, name="paymentforpractical_delete"),

    path('answer_list/', views.answer_list, name="answer_list"),
    path('answer_create/', views.answer_create, name="answer_create"),
    path('<int:pk>answer_edit/', views.answer_edit, name="answer_edit"),
    path('<int:pk>/answer_delete/', views.answer_delete, name="answer_delete"),

    path('question_list/', views.question_list, name="question_list"),
    path('question_create/', views.question_create, name="question_create"),
    path('<int:pk>question_edit/', views.question_edit, name="question_edit"),
    path('<int:pk>/question_delete/', views.question_delete, name="question_delete"),

    path('question_list/', views.question_list, name="question_list"),
    path('question_create/', views.question_create, name="question_create"),
    path('<int:pk>question_edit/', views.question_edit, name="question_edit"),
    path('<int:pk>/question_delete/', views.question_delete, name="question_delete"),

    path('bilet_list/', views.bilet_list, name="bilet_list"),
    path('bilet_create/', views.bilet_create, name="bilet_create"),
    path('<int:pk>bilet_edit/', views.bilet_edit, name="bilet_edit"),
    path('<int:pk>/bilet_delete/', views.bilet_delete, name="bilet_delete"),

    path('savol_list/', views.savol_list, name="savol_list"),
    path('savol_create/', views.savol_create, name="savol_create"),
    path('<int:pk>savol_edit/', views.savol_edit, name="savol_edit"),
    path('<int:pk>/savol_delete/', views.savol_delete, name="savol_delete"),

    path('javob_list/', views.javob_list, name="javob_list"),
    path('javob_create/', views.javob_create, name="javob_create"),
    path('<int:pk>javob_edit/', views.javob_edit, name="javob_edit"),
    path('<int:pk>/javob_delete/', views.javob_delete, name="javob_delete"),

    path('result_list/', views.result_list, name="result_list"),
    path('result_create/', views.result_create, name="result_create"),
    path('<int:pk>result_edit/', views.result_edit, name="result_edit"),
    path('<int:pk>/result_delete/', views.result_delete, name="result_delete"),

    path('resultquiz_list/', views.resultquiz_list, name="resultquiz_list"),
    path('resultquiz_create/', views.resultquiz_create, name="resultquiz_create"),
    path('<int:pk>resultquiz_edit/', views.resultquiz_edit, name="resultquiz_edit"),
    path('<int:pk>/resultquiz_delete/', views.resultquiz_delete, name="resultquiz_delete"),

    path('attempt_list/', views.attempt_list, name="attempt_list"),
    path('attempt_create/', views.attempt_create, name="attempt_create"),
    path('<int:pk>attempt_edit/', views.attempt_edit, name="attempt_edit"),
    path('<int:pk>/attempt_delete/', views.attempt_delete, name="attempt_delete"),

    path('resultjavob_list/', views.resultjavob_list, name="resultjavob_list"),
    path('resultjavob_create/', views.resultjavob_create, name="resultjavob_create"),
    path('<int:pk>resultjavob_edit/', views.resultjavob_edit, name="resultjavob_edit"),
    path('<int:pk>/resultjavob_delete/', views.resultjavob_delete, name="resultjavob_delete"),

    path('checktestcolor_list/', views.checktestcolor_list, name="checktestcolor_list"),
    path('checktestcolor_create/', views.checktestcolor_create, name="checktestcolor_create"),
    path('<int:pk>checktestcolor_edit/', views.checktestcolor_edit, name="checktestcolor_edit"),
    path('<int:pk>/checktestcolor_delete/', views.checktestcolor_delete, name="checktestcolor_delete"),

    path('signcategory_list/', views.signcategory_list, name="signcategory_list"),
    path('signcategory_create/', views.signcategory_create, name="signcategory_create"),
    path('<int:pk>signcategory_edit/', views.signcategory_edit, name="signcategory_edit"),
    path('<int:pk>/signcategory_delete/', views.signcategory_delete, name="signcategory_delete"),

    path('sign_list/', views.sign_list, name="sign_list"),
    path('sign_create/', views.sign_create, name="sign_create"),
    path('<int:pk>sign_edit/', views.sign_edit, name="sign_edit"),
    path('<int:pk>/sign_delete/', views.sign_delete, name="sign_delete"),

    # __________User Ulrs____________--
    path('region_list/', views.region_list, name="region_list"),
    path('region_create/', views.region_create, name="region_create"),
    path('<int:pk>/region_edit/', views.region_edit, name="region_edit"),
    path('<int:pk>/region_delete/', views.region_delete, name="region_delete"),

    path('district_list/', views.district_list, name="district_list"),
    path('district_create/', views.district_create, name="district_create"),
    path('<int:pk>district_edit/', views.district_edit, name="district_edit"),
    path('<int:pk>/district_delete/', views.district_delete, name="district_delete"),

    path('educationcategory_list/', views.educationcategory_list, name="educationcategory_list"),
    path('educationcategory_create/', views.educationcategory_create, name="educationcategory_create"),
    path('<int:pk>/educationcategory_edit/', views.educationcategory_edit, name="educationcategory_edit"),
    path('<int:pk>/educationcategory_delete/', views.educationcategory_delete, name="educationcategory_delete"),

    path('maktab_list/', views.list_schoool, name="maktab_list"),
    path('maktab_create/', views.school_create, name="maktab_create"),
    path('maktab_edit/<int:pk>/', views.school_edit, name="maktab_edit"),
    path('maktab_delete/<int:pk>/', views.school_delete, name="maktab_delete"),


    path('user_list/', views.user_list, name="user_list"),
    path('user_create/', views.user_create, name="user_create"),
    path('<int:pk>/user_edit/', views.user_edit, name="user_edit"),
    path('<int:pk>/user_delete/', views.user_delete, name="user_delete"),

    path('group_list/', views.group_list, name="group_list"),
    path('group_create/', views.group_create, name="group_create"),
    path('<int:pk>/group_edit/', views.group_edit, name="group_edit"),
    path('<int:pk>/group_delete/', views.group_delete, name="group_delete"),

    path('contact_list/', views.contact_list, name="contact_list"),
    path('contact_create/', views.contact_create, name="contact_create"),
    path('<int:pk>contact_edit/', views.contact_edit, name="contact_edit"),
    path('<int:pk>/contact_delete/', views.contact_delete, name="contact_delete"),

    path('pay_list/', views.pay_list, name="pay_list"),
    path('pay_create/', views.pay_create, name="pay_create"),
    path('<int:pk>/pay_edit/', views.pay_edit, name="pay_edit"),
    path('<int:pk>/pay_delete/', views.pay_delete, name="pay_delete"),

    path('referral_list/', views.referral_list, name="referral_list"),
    path('referral_create/', views.referral_create, name="referral_create"),
    path('<int:pk>referral_edit/', views.referral_edit, name="referral_edit"),
    path('<int:pk>/referral_delete/', views.referral_delete, name="referral_delete"),

    path('attendance_list/', views.attendance_list, name="attendance_list"),
    path('attendance_create/', views.attendance_create, name="attendance_create"),
    path('<int:pk>/attendance_edit/', views.attendance_edit, name="attendance_edit"),
    path('<int:pk>/attendance_delete/', views.attendance_delete, name="attendance_delete"),

    path('rating_list/', views.rating_list, name="rating_list"),
    path('rating_create/', views.rating_create, name="rating_create"),
    path('<int:pk>/rating_edit/', views.rating_edit, name="rating_edit"),
    path('<int:pk>/rating_delete/', views.rating_delete, name="rating_delete"),

    path('video_list/', views.video_list, name="video_list"),
    path('video_create/', views.video_create, name="video_create"),
    path('<int:pk>/video_edit/', views.video_edit, name="video_edit"),
    path('<int:pk>/video_delete/', views.video_delete, name="video_delete"),

    path('category_list/', views.category_list, name="category_list"),
    path('category_create/', views.category_create, name="category_create"),
    path('<int:pk>/category_edit/', views.category_edit, name="category_edit"),
    path('<int:pk>/category_delete/', views.category_delete, name="category_delete"),

    path('subject_list/', views.subject_list, name="subject_list"),
    path('subject_create/', views.subject_create, name="subject_create"),
    path('<int:pk>/subject_edit/', views.subject_edit, name="subject_edit"),
    path('<int:pk>/subject_delete/', views.subject_delete, name="subject_delete"),



]
