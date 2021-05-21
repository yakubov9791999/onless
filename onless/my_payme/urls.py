from django.urls import path
from my_payme import views

urlpatterns = [
    path('card/create/', views.CardCreateApiView.as_view(), name='card_create'),
    path('card/verify/', views.CardVerifyApiView.as_view(), name='card_verify'),
    path('payment/', views.PaymentApiView.as_view(), name='payment'),

]
