from django.db import models
from django.urls import reverse
from user.models import *
from quiz.models import User

SECTION_CHOICES = (
    ('1', "Yo'l harakati qoidalari"),
    ('2', "Avtomobil tuzilishi"),
    ('3', "Avtomobilni xavfsiz boshqarish"),
    ('4', "Birinchi tibbiy yordam"),
)


class MainSection(models.Model):
    title = models.CharField(choices=SECTION_CHOICES, max_length=30)
    photo = models.ImageField(upload_to='photo/%Y-%m-%d/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video_mainsection_detail_url', kwargs={'id': self.id})

    class Meta:
        verbose_name = "Asosiy bo'lim"
        verbose_name_plural = "Asosiy bo'limlar"


class VideoSection(models.Model):
    title = models.CharField(max_length=100)
    mainsection = models.ForeignKey(MainSection, on_delete=models.PROTECT, related_name='video_section')
    photo = models.ImageField(upload_to='photo/%Y-%m-%d/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video_section_detail_url', kwargs={'id': self.id})

    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"


# asosiy bo'lim ichiga biriktirilgan bo'lim
class VideoCategory(models.Model):
    title = models.CharField(max_length=100)
    section = models.ForeignKey(VideoSection, on_delete=models.PROTECT, related_name='video_category')
    photo = models.ImageField(upload_to='photo/%Y-%m-%d/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video_category_detail_url', kwargs={'id': self.id})

    class Meta:
        verbose_name = "Video Bo'lim"
        verbose_name_plural = "Video Bo'limlar"


class Video(models.Model):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(VideoCategory, on_delete=models.PROTECT, null=True, related_name='videos')
    is_free = models.BooleanField(
        default=True)  # video bepul bo'lsa, pul to'lamagan foydalanuvchiga foydalanishga ruxsat etadi
    likes = models.ManyToManyField(User, related_name='rating_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='rating_dislikes', blank=True)
    video = models.FileField(upload_to='video/%Y-%m-%d/')
    photo = models.ImageField(upload_to='photo/%Y-%m-%d/')
    pub_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video_detail_url', kwargs={'id': self.id})

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videolar"


class ViewComplete(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_view_complete')
    user = models.ForeignKey(User, related_name='user_view_complete', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ko'rilgan video"
        verbose_name_plural = "Ko'rilgan videolar"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    video = models.ForeignKey(Video, on_delete=models.PROTECT)
    text = models.TextField(max_length=800)


class Files(models.Model):
    title = models.CharField(max_length=100, )
    src = models.FileField(upload_to='file/%Y-%m-%d/')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
