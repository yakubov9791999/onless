from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from quiz.models import *
from user.models import School
from user.views import *
from video.models import *
from video.forms import *

def landing_page(request):
    return render(request, 'landing/index.html')


@login_required
def home(request):
    if request.user.role == "4":  # agarda role o'quvchi  bo'lsa
        if request.user.avatar == '' and request.user.birthday == '' and request.user.gender == '':
            return redirect(profil_edit)
        else:
            return redirect(mainsections_list)

    elif request.user.role == "3":  # agarda role o'qituvchi  bo'lsa
        if request.user.avatar == '' and request.user.birthday == '' and request.user.gender == '':
            return redirect(profil_edit)
        else:
            return redirect(groups_list)


    elif request.user.role == "2":  # agarda role Direktor  bo'lsa
        if request.user.avatar == '' and request.user.birthday == '' and request.user.gender == '':
            return redirect(profil_edit)
        else:
            return redirect(groups_list)

    elif request.user.role == "1":  # agarda role inspeksiya  bo'lsa
        # schools = School.objects.filter(region=request.user.district.region)
        return render(request, 'inspecion/schools_list.html', {
            # 'schools': schools,
        })



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
    context = {
        'mainsections': mainsections
    }
    return render(request, 'video/mainsections_list.html', context)


@login_required
def mainsection_detail(request, id):
    mainsection = MainSection.objects.get(id=id)
    context = {
        'mainsection': mainsection
    }
    for section in mainsection.video_section.all():
        context.update(section=section)
    return render(request, 'video/mainsection_detail.html', context)


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
    results = ResultQuiz.objects.filter(question__in=questions, question__video=video, user=request.user)
    return render(request, 'video/video_detail.html', {
        'video': video,
        'questions': questions,
        'results': results
    })

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

        mainsections = MainSection.objects.all()
        sections = VideoSection.objects.all()
        categories = VideoCategory.objects.all()
        context = {
            'form': form,
            'mainsections': mainsections,
            'sections': sections,
            'categories': categories,
        }
        return render(request, 'video/add_video.html', context)
    else:
        return render(request, 'inc/404.html')

@login_required
def myvideos_list(request):
    videos = Video.objects.all()
    print(videos)
    context = {
        'videos': videos
    }
    return render(request, 'video/myvideos_list.html', context)