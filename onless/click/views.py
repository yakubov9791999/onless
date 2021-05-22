from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from clickuz import ClickUz
from django.shortcuts import redirect, get_object_or_404
from clickuz.views import ClickUzMerchantAPIView
from clickuz import ClickUz
from django.urls import reverse_lazy

from click.models import Order
from onless.telegram_bot import send_message_to_developer
from user.models import User


@login_required
def create_order_url(request):
    try:
        if request.GET:
            amount = request.GET.get('amount')
            user = get_object_or_404(User, id=request.user.id)
            order = Order.objects.create(amount=amount,user=user)
            url = ClickUz.generate_url(order_id=order.id, amount=amount,return_url='http://onless.uz/user/sms-settings/')

        return redirect(url)
    except:
        messages.error(request, 'Xatolik yuz berdi! Sahifani yangilab qayta urinib ko\'ring!')
        return redirect(reverse_lazy('user:sms_settings'))

class OrderCheckAndPayment(ClickUz):
    def check_order(self, order_id: str, amount: str):
        send_message_to_developer('check   order_id ' + order_id + ' ' + 'amount ' + amount)
        if order_id:
            try:
                get_object_or_404(Order, id=order_id)
                return self.ORDER_FOUND
            except:
                return self.ORDER_NOT_FOUND


    def successfully_payment(self, order_id: str, transaction: object):
        send_message_to_developer('successfully_payment  order_id ' + order_id + 'transaction '+ transaction)
        order = get_object_or_404(Order, id=order_id)
        send_message_to_developer('successfully_payment2  order' + order)

class TestView(ClickUzMerchantAPIView):
    VALIDATE_CLASS = OrderCheckAndPayment


def success_order(request):
    send_message_to_developer('success_order')


