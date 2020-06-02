from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from user.forms import AuthenticationForm
from user.models import User
from video.views import video_lessons

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.get(username=username, password=password)
            print(user)
            # user = authenticate(username=username, password=password)
            if user is not None:
                return redirect(video_lessons)
            else:
                messages.error(request, "Invalid username or password")
        else:
            print('ne valid')
            messages.error(request, "Invalid username or password")
    return redirect(video_lessons)


