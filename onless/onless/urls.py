"""onless URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include
from django.conf import settings
from django.views.static import serve

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
                  path('yoz/', admin.site.urls),
                  path('', include('landing.urls')),
                  path('video/', include('video.urls')),
                  path('sign/', include('sign.urls')),
                  path('user/', include('user.urls')),
                  path('quiz/', include('quiz.urls')),
                  path('practical/', include('practical.urls')),
                  path('accounts/', include('allauth.urls')),
                  # path('payments/', include('payments.urls')),
                  # path('payments/', include('click.urls')),
                  # path('paycom/', TestView.as_view()),
                  path('payme/', include('paycom.urls')),
                  path('click/', include('click.urls')),
                  # path('summernote/', include('django_summernote.urls')),
                  path('sentry-debug/', trigger_error),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



