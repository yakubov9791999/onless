from django.db import models
from django.urls import reverse
from user.models import *



class Category(models.Model):
    categories = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True, related_name='category_category')
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="category/%Y-%m-%d/")
    sort = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def get_parents(self):
        parents = []
        p = self.categories
        while p:
            parents.append(p)
            p = p.categories
        parents.reverse()
        return parents

    def get_absolute_url(self):
        return reverse('video:category_detail', kwargs={'id': self.id,})

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
    src = models.TextField('Mp4',max_length=5000, blank=True)
    src2 = models.TextField('Webm',max_length=5000, blank=True)
    photo = models.ImageField(upload_to='photo/%Y-%m-%d/')
    pub_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    sort = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('video_detail_url', kwargs={'id': self.id})

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videolar"
        ordering = ('sort',)

class ViewComplete(models.Model):
    video = models.ForeignKey(Video, on_delete=models.SET_NULL,null=True, blank=True, related_name='video_view_complete')
    user = models.ForeignKey(User, related_name='user_view_complete', on_delete=models.SET_NULL, null=True)
    time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.video)

    class Meta:
        verbose_name = "Ko'rilgan video"
        verbose_name_plural = "Ko'rilgan videolar"



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=800)


class Files(models.Model):
    title = models.CharField(max_length=100, )
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True)
    src = models.FileField(upload_to='file/%Y-%m-%d/')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_all = models.BooleanField(default=False)


class SignUpSchool(models.Model):
    name = models.CharField(max_length=100,)
    viloyat = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.CharField(max_length=500, blank=True)
    tuman = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.CharField(max_length=500)
    phone = models.CharField(max_length=100)
    select = models.BooleanField(default=False, verbose_name='Avtomaktab')
    is_active = models.BooleanField(default=False, verbose_name="M/o'")
    result = models.CharField(max_length=255, blank=True, verbose_name='Natija')
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Avtomaktab')
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now, blank=True)

    class Meta:
        verbose_name = 'Qabul'
        verbose_name_plural = 'Qabullar'

CATEGORY_CHOICES = (
    ("A", "A"),
    ("B", "B"),
    ("BC", "BC"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E"),
)


class Nabor(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORY_CHOICES, verbose_name='Toifasi', max_length=15, default="B")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=True, null=True)
    phone = models.CharField(max_length=100)
    phone2 = models.CharField(max_length=100, blank=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Avtomaktab')
    pub_date = models.DateTimeField(default=timezone.now, blank=True)
    passport = models.FileField(upload_to='document/%Y-%m-%d/', blank=True)
    is_start = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Nabor'
        verbose_name_plural = 'Naborlar'