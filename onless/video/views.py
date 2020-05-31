from django.http import HttpResponse
from django.shortcuts import render

from video.models import *


def home(request):
    videos = Video.objects.all()
    return render(request, 'base.html', {'videos': videos})

def add_duration(request):
    if request.is_ajax():
        ViewComplete.objects.create(video=2, user=3)

        message = "Yes, AJAX!"
    else:

        message = "Not Ajax0"

    return HttpResponse(message)