import datetime
import os
from uuid import uuid4
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator

def path_and_rename(instance, filename):
    upload_to = 'user_avatars/'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class UserManager(BaseUserManager):

    def _create_user(self, email, username, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise Http404
        if not username:
            raise Http404
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,  username, password, **extra_fields):
        return self._create_user(username, password, False, False, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        user = self._create_user(email, username, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class Region(models.Model):
    title = models.CharField('Nomi',max_length=255)
    sort = models.IntegerField(blank=True, default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Viloyat'
        verbose_name_plural = 'Viloyatlar'

class District(models.Model):
    title = models.CharField('Nomi',max_length=255)
    region = models.ForeignKey(Region, verbose_name='Tuman', on_delete=models.CASCADE)
    sort = models.IntegerField(blank=True, default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tuman'
        verbose_name_plural = 'Tumanlar'

class School(models.Model):
    title = models.CharField(verbose_name='Nomi',max_length=255)
    director_fio = models.CharField(verbose_name='Rahbar nomi',max_length=255, blank=True)
    phone = models.CharField('Tel',max_length=20, blank=True)
    logo = models.ImageField('Rasm',upload_to='school/')
    district = models.ForeignKey(District,verbose_name='Viloyat',on_delete=models.PROTECT, related_name='school_distrinct', null=True)
    region = models.ForeignKey(Region,verbose_name='Tuman', on_delete=models.PROTECT, related_name='school_region', null=True)
    reg_date = models.DateTimeField(auto_now_add=True)
    is_amet = models.BooleanField(default=False)


    def __str__(self):
        return self.title

CATEGORY_CHOICES = (
    ("A", "A"),
    ("B", "B"),
    ("BC", "BC"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E"),
)

class Group(models.Model):
    category = models.CharField(choices=CATEGORY_CHOICES, verbose_name='Toifasi', max_length=15, default="B")
    number = models.IntegerField()
    year = models.IntegerField(verbose_name="O'quv yili")
    teacher = models.ForeignKey('User',verbose_name="O'qituvchi", on_delete=models.PROTECT, related_name='group_teacher')
    school = models.ForeignKey(School, on_delete=models.PROTECT, verbose_name="Avtomaktab", related_name='groups', null=True)
    start = models.DateField(verbose_name="O'qish boshlanishi",auto_now=False)
    stop = models.DateField(verbose_name="O'qish tugashi",auto_now=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.category}-{self.number}"

    def get_absolute_url(self):
        return reverse('group_detail_url', kwargs={'id': self.id })

ROLE_CHOICES = (
    ("2", "Direktor"),
    ("3", "O'qituvchi"),
    ("4", "O'quvchi"),
    ("5", "Inspeksiya"),
)

GENDER_CHOICES = (
    ('M', 'Erkak'),
    ('W', 'Ayol'),
)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    role = models.CharField(choices=ROLE_CHOICES, max_length=15, default="4")
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, related_name='users', blank=True)
    address = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=254, unique=False, blank=True)
    avatar = models.ImageField(upload_to='user/', default='', blank=True)
    birthday = models.DateField( blank=True, null=True, default=datetime.date.today)
    username = models.CharField(max_length=30, unique=True, blank=True)
    phone = models.IntegerField(null=True, blank=True, unique=True, validators=[MaxValueValidator(999999999)])
    group = models.OneToOneField(Group, on_delete=models.PROTECT, related_name='group', blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    last_login = models.DateTimeField(null=True, auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=5)
    turbo = models.CharField(max_length=200, blank=True, null=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def __str__(self):
        return f"{self.name}"


class Contact(models.Model):
    name = models.CharField(max_length=60)
    text = models.CharField(max_length=5000)
    photo = models.ImageField(upload_to='contact/', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"