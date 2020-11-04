from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import random
from user.models import User
from .forms import *
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from .models import *


@login_required
def add_result(request):
    if request.is_ajax():
        if request.GET:
            user = get_object_or_404(User, id=request.user.id)
            question = get_object_or_404(Savol, id=request.GET.get('question'))
            answer = get_object_or_404(Javob, id=request.GET.get('answer'))
            try:
                result = ResultQuiz.objects.filter(question=question, user=user)
                result.delete()
                if not result.exists():
                    ResultQuiz.objects.create(question=question, user=user, answer=answer,is_last=True)
                    attempt = Attempt.objects.filter(user=user)
                    if not attempt:
                        Attempt.objects.create(user=user)
                else:
                    return HttpResponse('disabled')

                if answer.is_true == True:
                    return HttpResponse(True)
                else:
                    return HttpResponse(False)
            except IntegrityError:
                return HttpResponse("alert")


@login_required
def select_bilet(request):
    if request.GET:
        if request.GET['lang'] == 'uz' or request.GET['lang'] == 'kr' or request.GET['lang'] == 'ru':
            try:
                bilet = Bilet.objects.get(number=request.GET.get('bilet'), is_active=True)
                context = {}
                if int(str(bilet.number)) == 1:
                    # agar birinchi bilet bo'lsa
                    lang = request.GET['lang']
                    questions = Savol.objects.filter(is_active=True, bilet=bilet.id).extra(
                        select={'bilet_savol': 'CAST(bilet_savol AS INTEGER)'}).extra(order_by=['bilet_savol'])
                    context.update(questions=questions, lang=lang, bilet=bilet)

                # elif int(str(bilet.number)) == 70:
                #     # agar oxirgi bilet bo'lsa
                #     lang = request.GET['lang']
                #     savollar = Savol.objects.filter(is_active=True, bilet=bilet.id).extra(
                #         select={'bilet_savol': 'CAST(bilet_savol AS INTEGER)'}).extra(order_by=['bilet_savol'])
                #     context.update(savollar=savollar, lang=lang, bilet=bilet)
                else:
                    # 1 va 70 dan boshqa biletlar uchun
                    prev_bilet = int(str(bilet.number)) - 1

                    if CheckTestColor.objects.filter(user=request.user, bilet__number=prev_bilet).exists():
                        # bitta oldingi bilet yechilgan bo'lsa
                        lang = request.GET['lang']
                        questions = Savol.objects.filter(is_active=True, bilet=bilet.id).extra(
                            select={'bilet_savol': 'CAST(bilet_savol AS INTEGER)'}).extra(order_by=['bilet_savol'])
                        context.update(questions=questions, lang=lang, bilet=bilet)
                    else:
                        # bitta oldingi bilet yechilmagan bo'lsa
                        lang = request.GET['lang']
                        bilets = Bilet.objects.filter(is_active=True).order_by('number')
                        check_last = CheckTestColor.objects.filter(user=request.user).order_by(
                            'bilet__number').distinct().last()

                        if check_last:
                            check_last = int(str(check_last)) + 1
                            context.update(check_last=check_last)

                        context.update(lang=lang, bilets=bilets)
                        prev_bilet = int(request.GET['bilet']) - 1
                        if lang == 'ru':
                            msg = f"Чтобы перейти на этот билет, вам нужно освоить билет {prev_bilet}"
                        elif lang == 'kr':
                            msg = f"Ушбу билетга ўтиш учун {prev_bilet}-билетни ўзлаштиришингиз керак"
                        else:
                            msg = f"Ushbu biletga o'tish uchun {prev_bilet}-biletni o'zlashtirishingiz kerak"
                        messages.error(request, msg)
                        return render(request, 'quiz/select_bilet.html', context)

                if Bilet.objects.filter(Q(number__gte=bilet.number) & Q(is_active=True)).order_by("-number")[
                   0:1].get().number:
                    last_active_bilet = Bilet.objects.filter(Q(number__gte=bilet.number) & Q(is_active=True)).order_by(
                        "-number")[
                                        0:1].get().number
                    last_bilet = Bilet.objects.filter(number__gte=bilet.number).order_by("-number")[0:1].get().number
                    context.update(last_active_bilet=last_active_bilet - 1, last_bilet=last_bilet)
                    check_last = CheckTestColor.objects.filter(user=request.user).order_by(
                        'bilet__number').distinct().last()
                    if check_last:
                        check_last = int(str(check_last)) + 1
                        context.update(check_last=check_last)

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
        answer = get_object_or_404(Javob, id=request.GET['answer'])
        savol = get_object_or_404(Savol, id=request.GET['question'])

        if answer.is_true == True:
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
                    # get random 10 questions
                    queryset = tuple(
                        Savol.objects.filter(is_active=True, bilet__is_active=True).values_list('id', flat=True))
                    random_queryset = random.sample(queryset, 10)
                    questions = Savol.objects.filter(id__in=random_queryset)
                    context.update(questions=questions)
                    return render(request, 'quiz/imtihon_test.html', context)
                elif type == 'T':
                    bilets = Bilet.objects.filter(is_active=True).order_by('number')
                    context.update(bilets=bilets)

                    check_last = CheckTestColor.objects.filter(user=request.user).order_by(
                        'bilet__number').distinct().last()

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
        bilet = get_object_or_404(Bilet, number=request.GET['bilet'])
        user = get_object_or_404(User, id=request.user.id)

        check_color = CheckTestColor.objects.filter(user=user, bilet=bilet).count()
        if check_color < 2:
            color = CheckTestColor.objects.create(bilet=bilet, user=user)
        else:
            return False

    return HttpResponse()


@login_required
def reset_answers(request):
    # questions_id = request.POST.getlist('arr[]', [])
    # questions_id = [json.loads(item) for item in data]
    user = get_object_or_404(User, id=request.user.id)
    try:
        attempt = Attempt.objects.get(user=user)
        if attempt.allowed > attempt.solved:
            attempt.solved += 1
            attempt.save()

            results = ResultQuiz.objects.filter(user=user)
            results.delete()

            messages.success(request, 'Natijalaringiz muvaffqaiyatli o\'chirildi!')
            return render(request, 'user/pupil/pupil_result.html')
        else:
            messages.error(request, 'Sizda qayta topshirish imkoniyati mavjud emas!')
            return render(request, 'user/pupil/pupil_result.html')
    except ObjectDoesNotExist:
        messages.warning(request, 'Sizda natijalar mavjud emas!')
        return render(request, 'user/pupil/pupil_result.html')
