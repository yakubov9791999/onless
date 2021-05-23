from django.urls import path

from .payme import *

app_name = 'paycom'
urlpatterns = [
    path('api/', PayMeView.as_view(), name='api'),
    path('create-paycom-url-via-order/', create_paycom_url_via_order, name='create_paycom_url_via_order'),
]
