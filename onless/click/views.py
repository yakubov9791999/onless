from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from clickuz import ClickUz
from django.shortcuts import redirect
from clickuz.views import ClickUzMerchantAPIView
from clickuz import ClickUz
from click.models import Order
from onless.telegram_bot import send_message_to_developer


@login_required
def create_order_url(request):
    order = Order.objects.create(amount=1000,user=request.user)
    url = ClickUz.generate_url(order_id=order.id, amount=order.amount,return_url='http://onless.uz/click/success/')
    return redirect(url)

class OrderCheckAndPayment(ClickUz):
    def check_order(self, order_id: str, amount: str):
        send_message_to_developer('CHECK ORDER')
        return self.ORDER_FOUND

    def successfully_payment(self, order_id: str, transaction: object):
        send_message_to_developer('SUCCESSFULLY PAYMENT')
        return HttpResponse('SUCCESSFULLY PAYMENT')

class TestView(ClickUzMerchantAPIView):
    VALIDATE_CLASS = OrderCheckAndPayment


def success_order(request):
    return HttpResponse(request.GET)