from django import template
from django.shortcuts import get_object_or_404

from quiz.models import *
from user.models import *

register = template.Library()

@register.simple_tag()
def pupil_result(id):
    pupil = get_object_or_404(User, id=id)
    old_answer_count = ResultQuiz.objects.filter(user=pupil).count()
    new_answer_count = Result.objects.filter(user=pupil).count()

    question_total_count = Savol.objects.filter(is_active=True, video__isnull=False).count()

    old_answer_true = ResultQuiz.objects.filter(user=pupil, answer__is_true=True).count()
    new_answer_true = Result.objects.filter(user=pupil, answer__is_true=True).count()

    old_answer_false = ResultQuiz.objects.filter(user=pupil, answer__is_true=False).count()
    new_answer_false = Result.objects.filter(user=pupil, answer__is_true=False).count()

    answer_true = int(old_answer_true) + int(new_answer_true)
    answer_false = int(old_answer_false) + int(new_answer_false)
    answer_count = int(old_answer_count) + int(new_answer_count)
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


@register.simple_tag
def get_bilet_color(bilet_id, user_id):
    bilet = get_object_or_404(Bilet, id=bilet_id)
    user = get_object_or_404(User, id=user_id)
    check_color = CheckTestColor.objects.filter(user=user, bilet=bilet)
    if check_color:
        return True
    else:
        return False

@register.simple_tag
def get_true_answer(user_id, question_id, answer_id):
    user = get_object_or_404(User, id=user_id)
    question = get_object_or_404(Savol, id=question_id)
    answer = get_object_or_404(Javob, id=answer_id)
    result = Result.objects.filter(user=user,question=question, answer=answer).last()

    if result:
        if result.answer.is_true:
            return True
        else:
            return False
