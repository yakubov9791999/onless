from django.urls import path, include
from .views import *



urlpatterns = [
    path('add_result/', add_result , name='add_result_url'),
]