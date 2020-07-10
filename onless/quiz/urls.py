from django.urls import path, include
from .views import *

app_name = 'quiz'

urlpatterns = [
    path('add_result/', add_result, name='add_result'),
    path('tests/', tests_list, name='tests_list'),
    path('get-true-answer/', get_true_answer, name='get_true_answer'),
    path('select-lang/', select_lang, name='select_lang'),


]
