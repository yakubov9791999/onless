from django.forms import ModelForm

from .models import *

class AddResultForm(ModelForm):

    class Meta:
        model = ResultQuiz
        exclude = ('user', 'question', 'answer')