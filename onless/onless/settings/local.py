from onless.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         'NAME': 'bcloudintelekt_onless',
#         'USER': 'bcloudintelekt',
#         'PASSWORD': 'm6232971',
#         'HOST': 'localhost',
#         'PORT': '3306',
    }
}