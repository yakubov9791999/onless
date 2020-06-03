from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from user.forms import AuthenticationForm
from user.models import User
from video.views import video_lessons
from django.db import IntegrityError

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
        form = AddTeacherForm(data=request.POST)
        print(form.errors)
        if form.is_valid():
            if request.POST['phone']:
                try:
                    user= User.objects.create_user(
                        username=request.POST['phone'],
                        password=request.POST['phone'],
                        name=form.cleaned_data['name'],
                        phone=form.cleaned_data['phone'],
                        address=form.cleaned_data['address'],
                        driving_school=request.user.driving_school,
                        role='3',
                        gender=request.POST['gender'],
                        birthday=form.cleaned_data['birthday'],
                        is_superuser=False,
                    )
                    user.set_password(request.POST['phone'])
                    user.save()
                    messages.success(request, "O'qituvchi muvaffaqaiyatli qo'shildi")

                except IntegrityError:
                    messages.error(request, "Bunday loginli foydalanuvchi mavjud")
            else:
                messages.error(request, "Bu raqam allaqachon kiritilgan")
        else:
            messages.error(request, "Formani to'ldiring")
    else:
        messages.error(request, 'Hatolik')
    return render(request, 'user/add_teacher.html', )


def add_pupil(request):
    return render(request, 'user/add_pupil.html', )
