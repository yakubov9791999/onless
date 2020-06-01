from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from video.models import *

@login_required
def home(request):
    pass

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
def video_lessons(request):
    videos = Video.objects.all()
    return render(request, 'video/videos.html', {
        'videos': videos,
    })

@login_required
def vide_detail_view(request, pk):
    video = Video.objects.get(pk=pk)
    print(video)
    return render(request, 'video/detail.html', {
        'video': video,
    })
