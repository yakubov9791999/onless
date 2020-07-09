from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

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
    if request.user.role == '1' or request.user.role == '2' or request.user.role == '3' or request.user.role == '4' or request.user.role == '5':
        savollar = Savol.objects.filter(is_active=True)

        context = {
            'savollar': savollar
        }

        if request.is_ajax():
            javob = get_object_or_404(Javob, id=request.GET['javob'])
            if javob.is_true == True:
                return HttpResponse('#89e790')
            else:
                return HttpResponse('#ef6565')
        else:
            print('no')

        return render(request, 'quiz/tests_list.html', context)
    else:
        return render(request, 'inc/404.html')
