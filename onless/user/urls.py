from django.urls import path, include
from .views import *



urlpatterns = [
    path('', user_login, name='login'),

]