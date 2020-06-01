from django.db import models
from quiz.models import User


class Category(models.Model):
    title = models.CharField(max_length=255)
    is_free = models.BooleanField(
        default=True)  # video bepul bo'lsa, pul to'lamagan foydalanuvchiga foydalanishga ruxsat etadi

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"


class Video(models.Model):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=600)
    is_free = models.BooleanField(
        default=True)  # video bepul bo'lsa, pul to'lamagan foydalanuvchiga foydalanishga ruxsat etadi
    likes = models.ManyToManyField(User, related_name='rating_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='rating_dislikes', blank=True)
    video = models.FileField(upload_to='video/%Y-%m-%d/')
    photo = models.ImageField(upload_to='photo/%Y-%m-%d/')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videolar"


class ViewComplete(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_view_complete')
    user = models.IntegerField(default=1)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ko'rilgan video"
        verbose_name_plural = "Ko'rilgan videolar"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    video = models.ForeignKey(Video, on_delete=models.PROTECT)
    text = models.TextField(max_length=800)


