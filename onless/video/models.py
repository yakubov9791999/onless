from django.db import models
from django.urls import reverse
from user.models import *
from quiz.models import User


class Category(models.Model):
    categories = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True, related_name='category_category')
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="category/%Y-%m-%d/")
    sort = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('sort',)


class Video(models.Model):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='video_category',
                                 blank=True)
    is_free = models.BooleanField(
        default=True)  # video bepul bo'lsa, pul to'lamagan foydalanuvchiga foydalanishga ruxsat etadi
    likes = models.ManyToManyField(User, related_name='rating_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='rating_dislikes', blank=True)
    video = models.TextField(max_length=5000)
    photo = models.ImageField(upload_to='photo/%Y-%m-%d/')
    pub_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video_detail_url', kwargs={'id': self.id})

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videolar"


class ViewComplete(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_view_complete')
    user = models.ForeignKey(User, related_name='user_view_complete', on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ko'rilgan video"
        verbose_name_plural = "Ko'rilgan videolar"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=800)


class Files(models.Model):
    title = models.CharField(max_length=100, )
    src = models.FileField(upload_to='file/%Y-%m-%d/')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
