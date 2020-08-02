import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from cgitb import handler

from django.db.backends import mysql

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(kbqdmc#xti0zu85$^%$%^$^f)u_yg67oj1bdi2_1f6=qlxe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=False

ALLOWED_HOSTS = ['onless.uz',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': 'bcloudintelekt_onless',
        'USER': 'bcloudintelekt',
        'PASSWORD': 'sierus2971',
        'HOST': 'localhost',
        'PORT': '3306',

    }
}

STATICFILES_DIRS = [
# '/home/users/b/bcloudintelekt/domains/onless.uz/static',
    os.path.join(BASE_DIR, 'static',

     )
]

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/users/b/bcloudintelekt/domains/onless.uz/media'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')