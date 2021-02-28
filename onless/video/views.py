from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from quiz.models import *
from user.models import *

from user.views import *
from video.models import *
from video.forms import *





@login_required
def add_duration(request):
    if request.is_ajax():

        video_id = request.GET.get('video', None)
        video = Video.objects.get(id=video_id)

        views = ViewComplete.objects.filter(video=video, user=request.user)

        if not views:
            ViewComplete.objects.create(video=video, user=request.user)
        message = "Siz darsni muvaffaqiyatli tugatdingiz! Agarda yana qaytadan ko'rmoqchi bo'lsangiz, istalgan vaqtda buni amalga oshirishingiz mumkin"
        return message
    else:
        return False


@login_required
def categories_list(request):
    categories = Category.objects.filter(categories__isnull=True, is_active=True)

    return render(request, 'video/categories_list.html', {
        'categories': categories,
    })


@login_required
def category_detail(request, id):
    categories = Category.objects.filter(categories=id, is_active=True)

    return render(request, 'video/categories_list.html', {
        'categories': categories,

    })


@login_required
def videos_list(request, id):
    videos = Video.objects.filter(category=id, is_active=True)
    views = ViewComplete.objects.filter(video__in=videos)
    return render(request, 'video/videos_list.html', {
        'videos': videos,
    })


@login_required
def video_detail(request, id):
    video = get_object_or_404(Video, id=id)
    category = get_object_or_404(Category, video_category=video)
    parent_category = category.categories
    videos = Video.objects.filter(category=category)
    next_video = videos.filter(sort__gt=video.sort).first()
    questions = Savol.objects.filter(video=video, is_active=True)
    results = ResultQuiz.objects.filter(question__in=questions, question__video=video, user=request.user)

    context = {
        'video': video,
        'questions': questions,
        'results': results,
        'next_video': next_video
    }

    try:
        # shu kategoriya bo'yicha video bo'lmasa
        if not next_video:
            child_categories = Category.objects.filter(categories__isnull=False)
            next_child_category = child_categories.filter(sort__gt=category.sort).first()
            next_video = Video.objects.filter(category=next_child_category).order_by('sort').first()
            context.update(next_video=next_video)
            if not next_child_category:
                categories = Category.objects.filter(categories__isnull=True)
                if not parent_category:
                    next_parent_category = categories.filter(sort__gt=category.sort).first()
                    next_video = Video.objects.filter(category=next_parent_category).order_by('sort').first()
                    context.update(next_video=next_video)
                else:
                    next_parent_category = categories.filter(sort__gt=parent_category.sort).first()
                    next_video = Video.objects.filter(category=next_parent_category).order_by('sort').first()
                    context.update(next_video=next_video)
    # agar keyingi video bo'lmasa
    except AttributeError:
        pass

    return render(request, 'video/video_detail.html', context)



@login_required
def add_video(request):
    if request.user.role == '2' or request.user.role == '3':
        form = AddVideoForm()
        if request.POST:
            form = AddVideoForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                category = request.POST['category']
                form = form.save(commit=False)
                form.category_id = category
                form.save()
                messages.success(request, "Video muvaffaqiyatli qo'shildi")
            else:
                messages.error(request, "Formani to'ldiring !")
        else:
            form = AddVideoForm()

        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
        }
        return render(request, 'video/add_video.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def myvideos_list(request):
    videos = Video.objects.filter(school=request.user.school)
    context = {
        'videos': videos
    }
    return render(request, 'video/myvideos_list.html', context)

# def show_categories(request):
#     return render(request, 'inc/breadcumb.html', {'categories': Category.objects.all()})

