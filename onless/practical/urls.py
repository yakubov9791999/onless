from django.urls import path, include
from .views import *

app_name = 'practical'

urlpatterns = [
    path('add-car/', add_car, name='add_car'),
]
