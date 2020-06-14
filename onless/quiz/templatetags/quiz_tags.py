from django import template
from django.shortcuts import get_object_or_404

from quiz.models import *
from user.models import *

register = template.Library()

@register.simple_tag()
def pupil_result(id):
    pupil = get_object_or_404(User, id=id)
    answer_count = ResultQuiz.objects.filter(user=pupil).count()
    answer_true = ResultQuiz.objects.filter(user=pupil, answer__is_true=True).count()
    try:
        res = int(answer_true * 100 / answer_count)
    except ZeroDivisionError:
        res = 0
    return {
        'answer_count': answer_count,
        'answer_true': answer_true,
        'res': res
    }
