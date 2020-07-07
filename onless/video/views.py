from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from quiz.models import *
from user.models import School
from user.views import *
from user.views import profil_edit
from video.models import *
from video.forms import *


def landing_page(request):
    return render(request, 'landing/index.html')


def sign_up(request):
    regions = Region.objects.all()
    context = {
        'regions': regions
    }

    if request.POST:
        form = SignUpSchoolForm(request.POST)
        viloyat = Region.objects.get(id=request.POST.get('viloyat'))
        tuman = District.objects.get(id=request.POST.get('tuman'))
        print(form.errors)
        if form.is_valid():
            if request.POST['select'] == '1':
                form = form.save(commit=False)
                form.viloyat = viloyat
                form.tuman = tuman
                form.select = True
                form.save()
            elif request.POST['select'] == '0':
                form = form.save(commit=False)
                form.viloyat = viloyat
                form.select = False
                form.save()
            messages.success(request, 'Muvaffaqiyatli yuborildi !')
    return render(request, 'sign_up/index.html', context)


@login_required
def home(request):
    if request.user.role == "4" and request.user.school.is_block == False:  # agarda role o'quvchi  bo'lsa
        if request.user.avatar == '' and request.user.birthday == '' and request.user.gender == '':
            return redirect(reverse_lazy('user:edit_profil'))
        else:
            return redirect(reverse_lazy("user:history_pupil_view_video", kwargs={'id': request.user.id}))


    elif request.user.role == "1":  # agarda role inspeksiya bo'lsa
        if request.user.avatar == '' and request.user.birthday == '' and request.user.gender == '':
            return redirect(reverse_lazy('user:edit_profil'))
        else:
            schools = School.objects.filter(Q(region=request.user.school.region)& Q(is_active=True)).exclude(id=request.user.school.id)
            return render(request, 'user/inspection/schools_list.html', {
                'schools': schools,
            })

    elif request.user.role == "3" and request.user.school.is_block == False:  # agarda role o'qituvchi  bo'lsa
        if request.user.avatar == '' and request.user.birthday == '' and request.user.gender == '':
            return redirect(reverse_lazy('user:edit_profil'))
        else:
            return redirect(reverse_lazy('user:groups_list'))


    elif request.user.role == "2" and request.user.school.is_block == False:  # agarda role Direktor  bo'lsa
        if request.user.avatar == '' and request.user.birthday == '' and request.user.gender == '':
            return redirect(profil_edit)
        else:
            return redirect(reverse_lazy('user:workers_list'))

    elif request.user.role == "5" and request.user.school.is_block == False:  # agarda role Bugalter  bo'lsa
        if request.user.avatar == '' and request.user.birthday == '' and request.user.gender == '':
            return redirect(profil_edit)
        else:
            return redirect(reverse_lazy('user:bugalter_groups_list'))
    else:
        return render(request, 'inc/block.html')

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
    video = Video.objects.get(id=id)
    questions = Question.objects.filter(video=video, is_active=True)
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

def kirish(request):
    return HttpResponseRedirect(reverse('account_login'))  # or http response
