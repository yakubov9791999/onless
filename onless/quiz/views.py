from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import random
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
def select_bilet(request):
    if request.GET:
        bilet = get_object_or_404(Bilet, id=request.GET['bilet'])
        lang = request.GET['lang']
        savollar = Savol.objects.filter(is_active=True, bilet=bilet)
        context = {
            'savollar': savollar,
            'lang': lang,
            'bilet': bilet
        }
        return render(request, 'quiz/trenka_test.html', context)
    else:
        return render(request, 'quiz/select_bilet.html')



def get_true_answer(request):
    if request.is_ajax():
        javob = get_object_or_404(Javob, id=request.GET['javob'])
        savol = get_object_or_404(Savol, id=request.GET['savol'])

        if javob.is_true == True:
            return HttpResponse(True)
        else:
            return HttpResponse(False)



def select_lang(request):
    if request.GET:
        lang = request.GET['lang']
        context = {
            'lang': lang
        }
        return render(request, 'quiz/select_type.html', context)
    else:
        return render(request, 'quiz/select_lang.html')


def select_type(request):
    if request.GET:
        lang = request.GET['lang']
        type = request.GET['type']
        context = {
            'lang': lang
        }
        if type == 'I':
            #get random 10 questions
            queryset = tuple(Savol.objects.filter(is_active=True).values_list('id', flat=True))
            random_queryset = random.sample(queryset, 10)
            savollar = Savol.objects.filter(id__in=random_queryset)
            context.update(savollar=savollar)
            return render(request, 'quiz/imtihon_test.html', context)
        elif type == 'T':
            bilets = Bilet.objects.filter(is_active=True)
            context.update(bilets=bilets)
            return render(request, 'quiz/select_bilet.html', context)
        else:
            return render(request, 'quiz/select_type.html')
    else:
        return render(request, 'quiz/select_type.html')

