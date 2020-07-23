from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import random
from user.models import User
from .forms import *
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

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
        if request.GET['lang'] == 'uz' or request.GET['lang'] == 'kr' or request.GET['lang'] == 'ru':
            try:
                bilet = Bilet.objects.get(number=request.GET.get('bilet'), )
                lang = request.GET['lang']
                savollar = Savol.objects.filter(is_active=True, bilet=bilet)


                context = {
                    'savollar': savollar,
                    'lang': lang,
                    'bilet': bilet,
                }

                if Bilet.objects.filter(id__gt=bilet.id).order_by("-id")[0:1].get().id:
                    last_active_bilet = Bilet.objects.filter(id__gt=bilet.id).order_by("-id")[0:1].get().id
                    context.update(last_active_bilet=last_active_bilet-1)
                return render(request, 'quiz/trenka_test.html', context)

            except ObjectDoesNotExist:

                messages.error(request, 'Bunday bilet mavjud emas !')
                return render(request, 'quiz/select_lang.html')
        else:
            messages.error(request, 'Mavjud tillardan birini tanlang !')
            return render(request, 'quiz/select_lang.html')


    else:
        return render(request, 'quiz/select_bilet.html')


@login_required
def get_true_answer(request):
    if request.is_ajax():
        javob = get_object_or_404(Javob, id=request.GET['javob'])
        savol = get_object_or_404(Savol, id=request.GET['savol'])

        if javob.is_true == True:
            return HttpResponse(True)
        else:
            return HttpResponse(False)


@login_required
def select_lang(request):
    if request.GET:
        if request.GET['lang'] == 'uz' or request.GET['lang'] == 'kr' or request.GET['lang'] == 'ru':
            lang = request.GET['lang']
            context = {
                'lang': lang
            }
            return render(request, 'quiz/select_type.html', context)
        else:
            return render(request, 'quiz/select_lang.html')
    else:
        return render(request, 'quiz/select_lang.html')

@login_required
def select_type(request):
    if request.GET:
        if request.GET['lang'] == 'uz' or request.GET['lang'] == 'kr' or request.GET['lang'] == 'ru':
            if request.GET['type'] == 'I' or request.GET['type'] == 'T':
                lang = request.GET['lang']
                type = request.GET['type']

                context = {
                    'lang': lang
                }
                if type == 'I':
                    #get random 10 questions
                    queryset = tuple(Savol.objects.filter(is_active=True, bilet__is_active=True).values_list('id', flat=True))
                    random_queryset = random.sample(queryset, 10)
                    savollar = Savol.objects.filter(id__in=random_queryset)
                    context.update(savollar=savollar)
                    return render(request, 'quiz/imtihon_test.html', context)
                elif type == 'T':
                    bilets = Bilet.objects.filter(is_active=True)
                    context.update(bilets=bilets)

                    check_last = CheckTestColor.objects.filter(user=request.user).order_by('bilet').distinct().last()
                    if check_last:
                        check_last = int(str(check_last)) + 1
                        context.update(check_last=check_last)

                    return render(request, 'quiz/select_bilet.html', context)
            else:
                messages.error(request, "Bunday mashg'ulot rejimi mavjud emas !")
                return render(request, 'quiz/select_lang.html')
        else:
            messages.error(request, 'Mavjud tillardan birini tanlang !')
            return render(request, 'quiz/select_lang.html')
    else:
        return render(request, 'quiz/select_type.html')


@login_required
def get_bilet_color(request):
    if request.is_ajax():
        bilet = get_object_or_404(Bilet, id=request.GET['bilet'])
        user = get_object_or_404(User, id=request.user.id)

        check_color = CheckTestColor.objects.filter(user=user, bilet=bilet).count()
        if check_color < 5:
            color = CheckTestColor.objects.create(bilet=bilet,user=user)
        else:
            return False

    return HttpResponse()