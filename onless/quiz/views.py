from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from user.models import User
from .forms import *
from django.utils.datastructures import MultiValueDictKeyError


@login_required
def add_result(request):
    question = Question.objects.get(id=request.POST['question'])
    if request.POST:

        try:
            form = AddResultForm(request.POST)
            if form.is_valid():
                answer = Answer.objects.get(id=request.POST['answer'])

                user = User.objects.get(id=request.user.id)
                result = ResultQuiz.objects.filter(question=question, user=user)
                if not result.exists():
                    form = form.save(commit=False)
                    form.answer = answer
                    form.user = user
                    form.question = question
                    form.save()

                # if answer.is_true:
                #     messages.success(request, "Javobingiz to'g'ri")
                # else:
                #     messages.error(request, "Javobingiz noto'g'ri")
        except MultiValueDictKeyError:
            form = AddResultForm()  # shu joyida keyingi savolga o'tishni qilish kerak
    else:
        form = AddResultForm()
    next = request.POST['next'] + '#question' + str(question.id)
    return HttpResponseRedirect(next)


@login_required
def tests_list(request):
    questions = Question.objects.all()
    context = {
        'questions': questions
    }
    return render(request, 'quiz/tests_list.html', context)
