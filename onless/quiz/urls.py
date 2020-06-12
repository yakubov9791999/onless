from django.urls import path, include
from .views import *

app_name = 'quiz'

urlpatterns = [
    path('add_result/', add_result, name='add_result'),
]
