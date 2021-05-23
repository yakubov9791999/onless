from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from click.models import Order
from user.models import User, School
from .views import MerchantAPIView
from paycom import Paycom
from paycom import status

from onless.telegram_bot import send_message_to_developer


class CheckOrder(Paycom):
    def check_order(self, amount, account):
        send_message_to_developer(f'amount {amount}')
        # amount = amount / 100
        print(account)
        order_id = account['order']


        try:
            print(18)
            order = Order.objects.get(id=int(order_id))
            print(amount)
            print(type(amount))
            print(order.amount)
            print(type(order.amount))
            if int(order.amount) != int(amount):
                print(19)
                return status.INVALID_AMOUNT
            print(21)
            return status.ORDER_FOUND
        except Order.DoesNotExist:
            print(26)
            return status.ORDER_NOT_FOND

    def successfully_payment(self, account, transaction, *args, **kwargs):
        order_id = int(account)
        try:
            order = get_object_or_404(Order, id=order_id)
            school = get_object_or_404(School, id=order.user.school.id)
            school.money += int(order.amount)
            school.save()
            send_message_to_developer('successfully add payment from payme ' + school.title + ': ' + order.amount)
        except Order.DoesNotExist:
            send_message_to_developer('successfully add payment from payme, no order object not found: ' + order_id)

    def cancel_payment(self, account, transaction, *args, **kwargs):
        pass


class PayMeView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder


def create_paycom_url_via_order(request):
    try:
        if request.GET:
            amount = request.GET.get('amount')
            user = get_object_or_404(User, id=request.user.id)
            order = Order.objects.create(amount=amount,user=user,service='2')
            payme = Paycom()
            url = payme.create_initialization(order_id=order.id, amount=amount,return_url='http://onless.uz/user/sms-settings/')
            send_message_to_developer(url)
            return redirect(url)
        else:
            return redirect(reverse_lazy('user:sms_settings'))
    except Order.DoesNotExist:
        send_message_to_developer(f' order id #{order.id} \n error wrong order id from payme ')
        messages.error(request, 'Xatolik yuz berdi! Sahifani yangilab qayta urinib ko\'ring!')
        return redirect(reverse_lazy('user:sms_settings'))
