from django.http import HttpResponse
from django.shortcuts import render

from video.models import *


def home(request):
    pass

def add_duration(request):
    if request.is_ajax():
        ViewComplete.objects.create(video=2, user=3)

    return True


def video_lessons(request):
    videos = Video.objects.all()
    return render(request, 'video/videos.html', {
        'videos': videos,
    })
