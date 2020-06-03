from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from user.forms import AuthenticationForm
from user.models import User
from video.views import video_lessons


#
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")

    return redirect(video_lessons)


def add_teacher(request):
    if request.method == 'POST':
        form = AddTeacher(data=request.POST)
        if form.is_valid():
            a = request.POST['birthday']
            b = a.replace('-', '')
            form.password = b
            if not User.objects.filter(username=form.cleaned_data['phone']).exists():
                User.objects.create_user(
                    username=form.cleaned_data['phone'],
                    name=form.cleaned_data['name'],
                    password=form.password,
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    driving_school=request.user.driving_school,
                    role='3',
                    gender=request.POST['gender'],
                    is_superuser=False,

                )
            else:
                messages.error(request, "Bunday loginli foydalanuvchi mavjud")
        else:
            messages.error(request, "Formani to'ldiring")
    else:
        messages.error(request, 'Hatolik')
    return render(request, 'user/add_teacher.html', )


def add_pupil(request):
    return render(request, 'user/add_pupil.html', )
