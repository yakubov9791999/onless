from django.urls import path, include
from .views import *

app_name = 'landing'

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('home/', home, name='home'),

    path('qabul/', sign_up, name='sign_up'),
    path('kirish/', kirish, name='kirish')

]
