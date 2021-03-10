from paycomuz.views import MerchantAPIView
from paycomuz.methods_subscribe_api import Paycom
from django.urls import path

class CheckOrder(Paycom):
    def check_order(self, amount, account):
        if account:
            return self.ORDER_FOUND
        else:
            return self.ORDER_NOT_FOND

class TestView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder