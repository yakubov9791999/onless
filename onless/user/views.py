from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

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
