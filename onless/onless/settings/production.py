from .base import *

DEBUG = False

ALLOWED_HOSTS = ['onless.uz']

DATABASES = {
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': 'bcloudintelekt_onless',
        'USER': 'bcloudintelekt',
        'PASSWORD': 'm6232971',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

