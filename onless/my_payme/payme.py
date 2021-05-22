from click.models import Order
from .views import MerchantAPIView
from my_payme import Paycom
from my_payme import status

from onless.telegram_bot import send_message_to_developer


class CheckOrder(Paycom):
    def check_order(self, amount, account):
        send_message_to_developer(f'amount {amount}')
        amount = amount / 100
        order_id = account['order']
        try:
            order = Order.objects.get(id=order_id)
            if int(order.get_total_amount()) != int(amount):
                return status.INVALID_AMOUNT
            return status.ORDER_FOUND
        except Order.DoesNotExist:
            return status.ORDER_NOT_FOND

    def successfully_payment(self, account, transaction, *args, **kwargs):
        send_message_to_developer(f'succes payed {transaction} \n {account}')
        order_id = int(account)
        try:
            order = Order.objects.get(id=order_id)


        except Order.DoesNotExist:
            send_message_to_developer(
                f'order = {order_id}  \n transaction = {transaction} transaction be successfully but transaction model '
                f'object not created because accepted wrong order id payme ')

        message = f'transaction successfully #{order_id} trans {transaction} '
        send_message_to_developer(message)

    def cancel_payment(self, account, transaction, *args, **kwargs):
        pass


class PayMeView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder


def create_pay_me_url_via_order(order_id) -> str:
    try:
        order = Order.objects.get(id=order_id)
        order_amount = order.get_total_amount()
        payme = Paycom()
        url = payme.create_initialization(amount=order_amount, order_id=str(order_id), return_url='https://tutto.uz/')
        send_message_to_developer(f'{url}')
        return url
    except Order.DoesNotExist:
        send_message_to_developer(f' order id #{order_id} \n error wrong order id from payme ')
        return 'https://onless.uz/'
