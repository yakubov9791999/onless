from paycomuz.views import MerchantAPIView
from paycomuz.methods_subscribe_api import Paycom
from django.urls import path

class CheckOrder(Paycom):
    def check_order(self, amount, account):
        return self.ORDER_FOUND

class TestView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder