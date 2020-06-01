from django.db import models
from quiz.models import User


class Video(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=600)
    duration = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='rating_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='rating_dislikes', blank=True)
    src = models.FileField(upload_to='quiz/video/%Y-%m-%d/')
    views = models.ManyToManyField(User, related_name='video_views', blank=True)

    def __str__(self):
        return self.title


class ViewComplete(models.Model):
    video = models.IntegerField(default=1)
    user = models.IntegerField(default=1)
    time = models.DateTimeField(auto_now_add=True)
