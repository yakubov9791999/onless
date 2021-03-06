from django.db import models
from django.utils import timezone

from django_summernote.fields import SummernoteTextFormField, SummernoteTextField

from user.decorators import get_name
from .decorators import get_slug
from .validators import *
from user.models import *
from video.models import Video

class SignCategory(models.Model):
    title = models.CharField(max_length=255)
    sort = models.IntegerField(default=1, null=True)

    def __str__(self):
        return self.title



class Sign(models.Model):
    category = models.ForeignKey(SignCategory, on_delete=models.SET_NULL, related_name='sign_cateogories', null=True)
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=5000, blank=True)
    photo = models.ImageField(upload_to="sign/")
    sort = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class Subject(models.Model):
    short_title = models.CharField(verbose_name='Qisqa nomi',max_length=600)
    long_title = models.TextField(verbose_name='To\'liq nomi',)
    categories = models.ManyToManyField(EducationCategory, verbose_name='Toifasi', max_length=20,)
    sort = models.IntegerField(verbose_name='Tartibi',null=True, blank=True)
    created_date = models.DateTimeField(null=True,default=timezone.now, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.short_title

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
        ordering = ['sort']


class Theme(models.Model):
    title = models.TextField(verbose_name='Nomi',)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, related_name='subject_theme',null=True, blank=True)
    sort = models.SmallIntegerField(verbose_name='Tartibi',default=1)
    theme_order = models.CharField(verbose_name='Mavzu tartibi',null=True, blank=True, max_length=5)
    category = models.ForeignKey(EducationCategory,related_name='category_theme', on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(default=timezone.now, editable=False)
    lesson_time = models.SmallIntegerField(default=2)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Mavzu"
        verbose_name_plural = "Mavzular"
        ordering = ['sort']

class Schedule(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, related_name='theme_schedule', null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, related_name='subject_schedule', null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='teacher_schedule', null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_schedule', null=True)
    created_date = models.DateTimeField(editable=False, default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    date = models.DateField(verbose_name='Kuni', null=True,blank=True)
    lesson_time = models.SmallIntegerField(default=2)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='author_schedule', null=True)
    is_active = models.BooleanField(default=True)
    theme_order = models.CharField(verbose_name='Mavzu tartibi', null=True, blank=True, max_length=5)
    sort = models.IntegerField(default=1)

    def __str__(self):
        return str(self.theme)

    class Meta:
        verbose_name = "Dars jadvali"
        verbose_name_plural = "Dars jadvallari"
        ordering = ['sort']


def path_and_rename(instance, filename):
    upload_to = 'sign/materials/'
    ext = filename.split('.')[-1]
    # filetitle = filename.rsplit(',', 1)
    # get filename
    title = os.path.splitext(instance.title)[0]
    filename = get_slug(title)
    # set filename as random string
    filename = '{}.{}'.format(filename, ext)
        # filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class Material(models.Model):
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, blank=True)
    sort = models.IntegerField(default=1)
    file =models.FileField(upload_to=path_and_rename, validators=[validate_file_extension])
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='author_material')
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, related_name="school_material")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiallar"


# class TrafficRules(models.Model):
#     title = models.CharField(verbose_name="Mavzu nomi", max_length=255)
#     text = models.TextField(verbose_name="Mavzu matni", blank=True)
#     pub_date = models.DateTimeField(auto_now_add=True)
#     sort = models.IntegerField(default=0, blank=True, null=True)


#     def __str__(self):
#         return self.title

#     class Meta:
#         verbose_name = "Yo'l harakati qoidasi"
#         verbose_name_plural = "Yo'l harakati qoidalari"