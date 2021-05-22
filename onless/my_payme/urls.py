from django.urls import path

from .payme import PayMeView

app_name = 'payme'
urlpatterns = [

    path('', PayMeView.as_view()),

]
