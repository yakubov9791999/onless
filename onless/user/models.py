import os
from uuid import uuid4
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


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
            raise ValueError('Emailni kiritish majburiy')
        if not username:
            raise ValueError('Usernameni kiritish majburiy')
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

    def create_user(self, email, username, region, password, **extra_fields):
        return self._create_user(email, username, password, False, False, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        user = self._create_user(email, username, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class Region(models.Model):
    title = models.CharField(max_length=255)
    sort = models.IntegerField(blank=True, default=1)


class District(models.Model):
    title = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    sort = models.IntegerField(blank=True, default=1)


class DrivingSchool(models.Model):
    title = models.CharField(max_length=255)
    director_fio = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)


CATEGORY_CHOICES = (
    ("A", "A"),
    ("B", "B"),
    ("BC", "BC"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E"),
)

class Group(models.Model):
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=15, default="B")
    number = models.IntegerField()
    year = models.IntegerField()
    teacher = models.ForeignKey('User', on_delete=models.PROTECT)


ROLE_CHOICES = (
    ("1", "Admin"),
    ("2", "Direktor"),
    ("3", "O'qituvchi"),
    ("4", "O'quvchi"),
)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    role = models.CharField(choices=ROLE_CHOICES, max_length=15, default="4")
    driving_school = models.ForeignKey(DrivingSchool, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=254, unique=True, blank=True)
    birthday = models.DateTimeField(max_length=120, blank=True, null=True)
    username = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    last_login = models.DateTimeField(null=True, auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def __str__(self):
        return f"{self.username}"
