from django import template
from django.shortcuts import get_object_or_404

from quiz.models import *
from user.models import *

register = template.Library()

@register.simple_tag()
def pupil_result(id):
    pupil = get_object_or_404(User, id=id)
    answer_count = ResultQuiz.objects.filter(user=pupil).count()
    question_total_count = Question.objects.filter(is_active=True).count()
    answer_true = ResultQuiz.objects.filter(user=pupil, answer__is_true=True).count()
    answer_false = ResultQuiz.objects.filter(user=pupil, answer__is_true=False).count()
    try:
        res = int(answer_true * 100 / answer_count)
    except ZeroDivisionError:
        res = 0

    try:
        total_res = int(answer_true * 100 / question_total_count)
    except ZeroDivisionError:
        total_res = 0

    return {
        'answer_count': answer_count,
        'answer_true': answer_true,
        'res': res,
        'question_total_count': question_total_count,
        'total_res': total_res,
        'answer_false': answer_false
    }

@register.simple_tag()
def get_true_javob(savol_id):
    savol = get_object_or_404(Savol, id=savol_id)
    javoblar = Javob.objects.filter(savol=savol)
    context = {}
    try:
        context.update(javob_1=javoblar[0])
    except IndexError:
        pass

    try:
        context.update(javob_2=javoblar[1])
    except IndexError:
        pass

    try:
        context.update(javob_3=javoblar[2])
    except IndexError:
        pass

    try:
        context.update(javob_4=javoblar[3])
    except IndexError:
        pass

    try:
        context.update(javob_5=javoblar[4])
    except IndexError:
        pass

    try:
        context.update(javob_6=javoblar[5])
    except IndexError:
        pass
    return context


@register.simple_tag()
def get_true_javob_color(javob_id):
    javob = get_object_or_404(Javob, id=javob_id)
    if javob.is_true == True:
        return 'green'
    else:
        return 'red'