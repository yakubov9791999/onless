from django.urls import path, include
from .views import *

app_name = 'quiz'

urlpatterns = [
    path('add_result/', add_result, name='add_result'),
    path('get-true-answer/', get_true_answer, name='get_true_answer'),
    path('select-lang/', select_lang, name='select_lang'),
    path('select-type/', select_type, name='select_type'),
    path('select-bilet/', select_bilet, name='select_bilet'),
    path('get_bilet_color/', get_bilet_color, name='get_bilet_color'),
    path('reset-answers/', reset_answers, name='reset_answers'),

]
