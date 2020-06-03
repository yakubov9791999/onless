from django.urls import path, include
from .views import *



urlpatterns = [
    path('', user_login, name='login'),
    path('add_teacher/', add_teacher, name='add_teacher_url'),
    path('add_pupil/', add_pupil, name='add_pupil_url'),
]
