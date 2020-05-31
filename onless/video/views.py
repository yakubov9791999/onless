from django.shortcuts import render

from video.models import Video


def home(request):
    videos = Video.objects.all()
    return render(request, 'base.html', {'videos': videos})
