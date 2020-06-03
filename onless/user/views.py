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
            form.username = 'asasasdasd'
            form.driving_school_id = request.user.driving_school.id
            form.role = '3'
            form.phone = request.POST['phone']
            form.gender = 'M'
            form.save()
        else:
            print('ne valid')
            messages.error(request, "Formani to'ldiring")
    else:
        messages.error(request, 'Hatolik')
    return render(request, 'user/add_teacher.html', )

def add_pupil(request):
    return render(request, 'user/add_pupil.html', )