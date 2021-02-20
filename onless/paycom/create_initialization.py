from paycomuz.methods_subscribe_api import Paycom
paycom = Paycom()
url = paycom.create_initialization(amount=5000.00, order_id='197', return_url='https://onless.uz/payment-paymee/')
print(url)