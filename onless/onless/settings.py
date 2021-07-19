"""
salom
Django settings for onless project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from .api import SendSmsWithApi

try:
    from .local_settings import *
except ImportError:
    from .prod_settings import *

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://464e6f5a9d6a48bda9cc628ef9000c23@o732152.ingest.sentry.io/5784021",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# Application definition

INSTALLED_APPS = [
    # MyApp
    'user.apps.UserConfig',
    'quiz.apps.QuizConfig',
    'video.apps.VideoConfig',
    # django apps
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'video.templatetags',
    'sign',
    'practical',
    'payments',
    'click',
    'rest_framework',
    'landing',
    'django_summernote',
    'clickuz',
    'django_bootstrap_breadcrumbs',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'onless.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'onless.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/


PAYMENT_HOST = '81.177.139.231:443'
PAYMENT_USES_SSL = True  # set the True value if you are using the SSL
PAYMENT_MODEL = 'user.Payment'
# payment model format like this :: '<app_name>.<model_name>'
# add "click" to your variants
PAYMENT_VARIANTS = {
    'click': ('click.ClickProvider', {
        'merchant_id': 12584,
        'merchant_service_id': 17367,
        'merchant_user_id': 18969,
        'secret_key': 'tVhBORlLRo8AN'
    })

}

CLICK_SETTINGS = {
    'service_id': 17367,
    'merchant_id': 12584,
    'secret_key': 'tVhBORlLRo8AN',
    'merchant_user_id': 18969,
}

LANGUAGE_CODE = 'uz-UZ'

TIME_ZONE = 'Asia/Tashkent'

# SHORT_DATE_FORMAT = 'd/m/Y'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]
AUTH_USER_MODEL = 'user.User'
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
LOGIN_REDIRECT_URL = '/home/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
# This ensures you have all toolbar icons
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}

import pytz

ASIA_TASHKENT_TIMEZONE = pytz.timezone("Asia/Tashkent")
SMS_PRICE = 180
SMS_ADD_STEP = 10


BREADCRUMBS_TEMPLATE = "django_bootstrap_breadcrumbs/bootstrap4.html"

