from django import template
from django.shortcuts import get_object_or_404

from quiz.models import *
from user.models import *
from video.models import *

register = template.Library()

@register.simple_tag
def get_view_video(user_id, video_id):
    user = User.objects.get(id=user_id)
    video = Video.objects.get(id=video_id)
    view_this_video = ViewComplete.objects.filter(user=user, video=video)
    return view_this_video

@register.simple_tag()
def get_results(user_id, question_id, answer_id):
    user = User.objects.get(id=user_id)
    question = Question.objects.get(id=question_id)
    answer = Answer.objects.get(id=answer_id)
    result = ResultQuiz.objects.filter(user=user, question=question, answer=answer)
    return result

@register.simple_tag()
def get_answer(user_id, question_id):
    user = User.objects.get(id=user_id)
    question = Question.objects.get(id=question_id)
    result_quiz = ResultQuiz.objects.filter(user=user, question=question)
    return result_quiz

@register.simple_tag()
def get_views_count(user_id):
    user = get_object_or_404(User, id=user_id)
    videos_count = Video.objects.all().count()
    views_count = ViewComplete.objects.filter(user=user).distinct().count()
    not_view = videos_count - views_count
    return {
       'views_count': views_count,
        'not_view': not_view,
        'videos_count': videos_count
    }
