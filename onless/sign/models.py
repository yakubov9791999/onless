from django.db import models

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
    title = models.CharField(verbose_name='Nomi',max_length=600)
    category = models.CharField(verbose_name='Toifasi',choices=CATEGORY_CHOICES, max_length=20, default='A')
    sort = models.IntegerField(verbose_name='Tartibi',null=True, blank=True)
    created_date = models.DateTimeField(null=True,)
    updated_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='author_subject', null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school_subject', null=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"

class Schedule(models.Model):
    title = models.CharField(max_length=900)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, related_name='subject_schedule', null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_schedule', null=True)
    created_date = models.DateTimeField(editable=False, null=True, blank=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    date = models.DateField(verbose_name='Kuni', null=True,blank=True)
    start = models.CharField(verbose_name='Boshlanish vaqti', null=True, max_length=5)
    stop = models.CharField(verbose_name='Tugash vaqti', null=True,max_length=5)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='author_schedule', null=True)
    sort = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Dars jadvali"
        verbose_name_plural = "Dars jadvallari"


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