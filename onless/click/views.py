from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from clickuz import ClickUz
from django.shortcuts import redirect
from clickuz.views import ClickUzMerchantAPIView
from clickuz import ClickUz
from click.models import Order

@login_required
def create_order_url(request):
    order = Order.objects.create(amount=1000,user=request.user)
    url = ClickUz.generate_url(order_id=order.id, amount=order.amount,return_url='http://onless.uz/click/transaction/')
    return redirect(url)

class OrderCheckAndPayment(ClickUz):
    def check_order(self, order_id: str, amount: float):
        print('CHECK ORDER')
        print(order_id)
        print(amount)
        return self.ORDER_FOUND

    def successfully_payment(self, order_id: str, transaction: object):
        print('SUCCESSFULLY PAYMENT')
        print(order_id)
        print(transaction)
        return HttpResponse('SUCCESSFULLY PAYMENT')

class TestView(ClickUzMerchantAPIView):
    VALIDATE_CLASS = OrderCheckAndPayment