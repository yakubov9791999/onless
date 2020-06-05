from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from quiz.models import *
from video.models import *


@login_required
def home(request):
    return redirect(mainsections_list)


@login_required
def add_duration(request):
    if request.is_ajax():
        video_id = request.GET.get('video', None)
        video = Video.objects.get(id=video_id)
        if video:
            ViewComplete.objects.create(video=video, user=3)
        message = "Siz darsni muvaffaqiyatli tugatdingiz! Agarda yana qaytadan ko'rmoqchi bo'lsangiz, istalgan vaqtda buni amalga oshirishingiz mumkin"
        return message
    else:
        return False


@login_required
def mainsections_list(request):
    mainsections = MainSection.objects.all()

    return render(request, 'video/mainsections_list.html', {
        'mainsections': mainsections,
    })


@login_required
def mainsection_detail(request, id):
    mainsection = MainSection.objects.get(id=id)

    return render(request, 'video/mainsection_detail.html', {
        'mainsection': mainsection,
    })

@login_required
def categories_list(request):
    categories = VideoCategory.objects.all()

    return render(request, 'video/categories_list.html', {
        'categories': categories,
    })

@login_required
def category_detail(request, id):
    category = VideoCategory.objects.get(id=id)

    return render(request, 'video/category_detail.html', {
        'category': category,
    })

@login_required
def video_detail(request, id):
    video = Video.objects.get(id=id)
    questions = Question.objects.filter(video=video)
    return render(request, 'video/video_detail.html', {
        'video': video,
        'questions': questions,
    })



