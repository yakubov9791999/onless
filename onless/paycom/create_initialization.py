from paycomuz.methods_subscribe_api import Paycom

paycom = Paycom()
amount = '5000.00'
url = paycom.create_initialization(amount=amount, order_id='197', return_url='https://checkout.test.paycom.uz/api')
print(url)
