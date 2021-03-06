import json
import os
import random
import time
from types import FunctionType
import requests
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from onless.telegram_bot import send_message_to_developer

SUCCESS = 200
PROCESSING = 102
FAILED = 400
INVALID_NUMBER = 160
MESSAGE_IS_EMPTY = 170
SMS_NOT_FOUND = 404
SMS_SERVICE_NOT_TURNED = 600


class SendSmsWithApi:
    def __init__(self, user, message=None, subject=None, score=None, pay=None, payment=None, is_add_pupil=False,
                 is_edit_pupil=False, is_add_worker=False,
                 is_edit_worker=False, is_attendance=False, is_rating=False, is_payment=False):

        self.user = user
        self.phone = user.phone
        self.message = message
        self.subject = subject
        self.score = score
        self.pay = pay
        self.payment = payment
        self.is_add_pupil = is_add_pupil
        self.is_edit_pupil = is_edit_pupil
        self.is_add_worker = is_add_worker
        self.is_edit_worker = is_edit_worker
        self.is_attendance = is_attendance
        self.is_rating = is_rating
        self.is_payment = is_payment
        self.spend = None

    def get(self):
        status_code = self.custom_validation()
        if status_code == SUCCESS:
            message = self.clean_message(self.make_messages())
            # print(message)
            result = self.calculation_send_sms(message)
            if result == SUCCESS:
                # print(result, 43)
                return self.send_message(message)
            else:
                return result
        return status_code

    def custom_validation(self):
        if self.is_add_pupil:
            if not self.user.school.send_sms_add_pupil:
                return SMS_SERVICE_NOT_TURNED

        if self.is_edit_pupil:
            if not self.user.school.send_sms_edit_pupil:
                return SMS_SERVICE_NOT_TURNED

        if self.is_add_worker:
            if not self.user.school.send_sms_add_worker:
                return SMS_SERVICE_NOT_TURNED

        if self.is_edit_worker:
            if not self.user.school.send_sms_edit_worker:
                return SMS_SERVICE_NOT_TURNED

        if self.is_attendance:
            if not self.user.school.send_sms_attendance:
                return SMS_SERVICE_NOT_TURNED

        if self.is_rating:
            if not self.user.school.send_sms_rating:
                return SMS_SERVICE_NOT_TURNED

        if self.is_payment:
            if not self.user.school.send_sms_payment:
                return SMS_SERVICE_NOT_TURNED

        if not len(str(self.phone)) == 9:
            return INVALID_NUMBER

        if not any([self.is_add_pupil, self.is_edit_pupil, self.is_add_worker, self.is_edit_worker, self.is_attendance,
                    self.is_rating, self.is_payment]):
            if self.message == '' or self.message == None:
                return MESSAGE_IS_EMPTY
            else:
                self.message = self.clean_message(self.message)
        return SUCCESS

    def authorization(self):
        data = {
            'email': 'bcloudintelekt@gmail.com',
            'password': 'ddMFQPXTfQRuhj8nmNSyfLv6mniuSpBHxGj3ZEY5',
        }

        AUTHORIZATION_URL = 'http://notify.eskiz.uz/api/auth/login'

        r = requests.request('POST', AUTHORIZATION_URL, data=data)
        if r.json()['data']['token']:
            return r.json()['data']['token']
        else:
            return FAILED

    def send_message(self, message):
        token = self.authorization()
        # print(f"Token: {token}")
        if token == FAILED:
            return FAILED

        SEND_SMS_URL = "http://notify.eskiz.uz/api/message/sms/send"
        # STATUS_SMS_URL = "http://notify.eskiz.uz/api/message/sms/status/"

        PAYLOAD = {
            'mobile_phone': '998' + str(self.phone),
            'message': message,
            'from': '4546',
            'callback_url': 'http://afbaf9e5a0a6.ngrok.io/sms-api-result/'}

        FILES = [

        ]
        HEADERS = {
            'Authorization': f'Bearer {token}'
        }
        # print(f'message: {self.message}')
        r = requests.request("POST", SEND_SMS_URL, headers=HEADERS, data=PAYLOAD, files=FILES)
        if r.json()['status'] == 'error':
            self.user.school.sms_count = self.user.school.sms_count + self.spend
            self.user.school.save()
        # print(f"Eskiz: {r.json()}" )
        try:
            from user.models import Sms
            Sms.objects.create(school=self.user.school, sms_id=r.json()['id'], sms_count=self.spend, text=self.message,
                               phone=self.phone)
        except:
            send_message_to_developer("sms object create error")
        return r.status_code
        # return SUCCESS

    def clean_message(self, message):
        message = message.replace('??', 'ts').replace('??', 'ch').replace('??',
                                                                        'yu').replace(
            '??', 'a').replace('??', 'b').replace('??', "q").replace('??', "o'").replace('??', "g'").replace('??',
                                                                                                        "h").replace(
            '??',
            "x").replace(
            '??', 'v').replace('??', 'g').replace('??', 'd').replace('??',
                                                                  'e').replace(
            '??', 'yo').replace('??', 'j').replace('??', 'z').replace('??', 'i').replace('??', 'y').replace('??',
                                                                                                       'k').replace(
            '??', 'l').replace('??', 'm').replace('??', 'n').replace('??', 'o').replace('??', 'p').replace('??',
                                                                                                      'r').replace(
            '??', 's').replace('??', 't').replace('??', 'u').replace('??', 'sh').replace('??', 'sh').replace('??',
                                                                                                        'f').replace(
            '??', 'e').replace('??', 'i').replace('??', 'ya').replace('??', "o'").replace('??', "'").replace('??',
                                                                                                        "'").replace(
            '???', "'").replace('???', '"').replace('???', '"').replace(',', ',').replace('.', '.').replace(':', ':')
        # filter upper
        message = message.replace('??', 'Ts').replace('??', 'Ch').replace('??', 'Yu').replace(
            '??', 'A').replace('??', 'B').replace('??', "Q").replace('??', "G'").replace('??', "H").replace('??',
                                                                                                       "X").replace(
            '??', 'V').replace('??', 'G').replace('??', 'D').replace('??',
                                                                  'E').replace(
            '??', 'Yo').replace('??', 'J').replace('??', 'Z').replace('??', 'I').replace('??', 'Y').replace('??',
                                                                                                       'K').replace(
            '??', 'L').replace('??', 'M').replace('??', 'N').replace('??', 'O').replace('??', 'P').replace('??',
                                                                                                      'R').replace(
            '??', 'S').replace('??', 'T').replace('??', 'U').replace('??', 'Sh').replace('??', 'Sh').replace('??',
                                                                                                        'F').replace(
            '??', 'E').replace('??', 'Ya')
        return message

    def make_messages(self):
        if self.is_add_pupil:
            self.message = f"Hurmatli {self.user.name}! Siz {self.user.group.category}-{self.user.group.number} guruhiga o'qishga qabul qilindingiz. Videodarslarni ko'rish va imtihon testlariga tayyorlanish uchun http://onless.uz/kirish manziliga kiring. \nLogin: {self.user.username}\nParol: {self.user.turbo}\nQo'shimcha ma'lumot uchun:{self.user.school.phone}"
            return self.message
        elif self.is_edit_pupil:
            self.message = f"Hurmatli {self.user.name}! Sizning ma'lumotlaringiz tahrirlandi. http://onless.uz/kirish manziliga kiring. \nLogin: {self.user.username}\nParol: {self.user.turbo}\nQo'shimcha ma'lumot uchun:{self.user.school.phone}"
            return self.message
        elif self.is_add_worker:
            if self.user.role == '6':
                role = 'instruktor'
            elif self.user.role == '5':
                role = 'hisobchi'
            else:
                role = "o'qituvchi"

            self.message = f"Hurmatli {self.user.name}! Siz {self.user.school.title} da {role} lavozimida ro'yhatga olindingiz. http://onless.uz/kirish manziliga kiring. \nLogin: {self.user.username}\nParol: {self.user.turbo}\nQo'shimcha ma'lumot uchun:{self.user.school.phone}"
            return self.message
        elif self.is_edit_worker:
            self.message = f"Hurmatli {self.user.name}! Sizning ma'lumotlaringiz tahrirlandi. http://onless.uz/kirish manziliga kiring. \nLogin: {self.user.username}\nParol: {self.user.turbo}\nQo'shimcha ma'lumot uchun:{self.user.school.phone}"
            return self.message
        elif self.is_attendance:
            if self.subject:
                self.message = f"Hurmatli {self.user.name}! Bugun {self.subject.short_title} fanidan darsga qatnashmadingiz. Bu hol qayta takrorlansa guruh ro'yhatidan chetlashtirilasiz!\nQo'shimcha ma'lumot uchun:{self.user.school.phone}"
                return self.message
        elif self.is_rating:
            if self.subject and self.score:
                self.message = f"Hurmatli {self.user.name}! Bugun {self.subject.short_title} fanidan {self.score} bahosini oldingiz!\nQo'shimcha ma'lumot uchun:{self.user.school.phone}"
                return self.message
        elif self.is_payment:
            if self.pay and self.payment:
                self.message = f"Hurmatli {self.user.name}! Avtomaktabga {self.pay} so???m to???lov qildingiz! Jami to???lovingiz {self.payment} so???m. Toifa bo???yicha {self.user.group.price - int(self.payment)} so???m qarzdorligingiz qoldi!\nQo'shimcha ma'lumot uchun:{self.user.school.phone}"
                return self.message
        else:
            return self.message

    def calculation_send_sms(self, message):
        try:
            length = len(message)
            # print(f"length: {length}")
            if length:
                if length >= 0 and length <= 160:
                    self.spend = 1
                elif length > 160 and length <= 306:
                    self.spend = 2
                elif length > 306 and length <= 459:
                    self.spend = 3
                elif length > 459 and length <= 612:
                    self.spend = 4
                elif length > 612 and length <= 765:
                    self.spend = 5
                elif length > 765 and length <= 918:
                    self.spend = 6
                elif length > 918 and length <= 1071:
                    self.spend = 7
                elif length > 1071 and length <= 1224:
                    self.spend = 8
                else:
                    self.spend = 30

                # print(f"spend: {self.spend}")

                if self.user.school.sms_count >= self.spend:
                    self.user.school.sms_count = self.user.school.sms_count - self.spend
                    self.user.school.save()
                    return SUCCESS
                return SMS_NOT_FOUND
        except:
            return FAILED


def sms_api_result(request):
    try:
        send_message_to_developer(f"{request}")
    except:
        if request:
            send_message_to_developer('sms from SmsApi, Eskiz.uz send sms')


class GetStatusSms:
    def __init__(self, id):
        self.id = id

    def authorization(self):
        data = {
            'email': 'bcloudintelekt@gmail.com',
            'password': 'ddMFQPXTfQRuhj8nmNSyfLv6mniuSpBHxGj3ZEY5',
        }

        AUTHORIZATION_URL = 'http://notify.eskiz.uz/api/auth/login'

        r = requests.request('POST', AUTHORIZATION_URL, data=data)
        if r.json()['data']['token']:
            return r.json()['data']['token']
        else:
            return FAILED

    def get(self):

        token = self.authorization()

        CHECK_STATUS_URL = 'http://notify.eskiz.uz/api/message/sms/status/' + str(self.id)

        HEADERS = {
            'Authorization': f'Bearer {token}'
        }

        r = requests.request("GET", CHECK_STATUS_URL, headers=HEADERS)
        if r.json()['status'] == 'success':
            if r.json()['message']['status'] == 'DELIVRD' or r.json()['message']['status'] == 'TRANSMTD':
                return SUCCESS
            elif r.json()['message']['status'] == 'EXPIRED':
                return FAILED
            else:
                return PROCESSING


class SendSmsWithPlayMobile:
    def __init__(self,
                 user,
                 message=None,
                 is_add_pupil=False,
                 is_edit_pupil=False,
                 is_add_worker=False,
                 is_edit_worker=False,
                 is_attendance=False,
                 is_rating=False,
                 is_payment=False,

                 subject=None,
                 score=None,
                 pay=None,
                 payment=None,
                 ):

        self.phone = user.phone
        self.message = message
        self.spend = None
        self.message_id = random.randint(100000000, 999999999)
        self.username = os.getenv('PLAY_MOBILE_USERNAME')
        self.password = os.getenv('PLAY_MOBILE_PASSWORD')
        self.is_add_pupil = is_add_pupil
        self.is_edit_pupil = is_edit_pupil
        self.is_add_worker = is_add_worker
        self.is_edit_worker = is_edit_worker
        self.is_attendance = is_attendance
        self.is_rating = is_rating
        self.is_payment = is_payment
        self.user = user
        self.subject = subject
        self.score = score
        self.pay = pay
        self.payment = payment

    def get(self):
        step1 = self.custom_validation()
        if step1['status'] == SUCCESS:
            maked_message = self.make_messages()
            message = self.clean_message(maked_message)
            step2 = self.calculation_send_sms(message)
            if step2['status'] == SUCCESS:
                return self.send_message(message)
            else:
                return {'status': FAILED, 'result': step2['result']}
        else:
            return {'status': FAILED, 'result': step1['result']}

    def custom_validation(self):
        if self.is_add_pupil:
            if not self.user.school.send_sms_add_pupil:
                return {'status': FAILED, 'result': "Sms xizmati o'chirilgan!"}

        if self.is_edit_pupil:
            if not self.user.school.send_sms_edit_pupil:
                return {'status': FAILED, 'result': "Sms xizmati o'chirilgan!"}

        if self.is_add_worker:
            if not self.user.school.send_sms_add_worker:
                return {'status': FAILED, 'result': "Sms xizmati o'chirilgan!"}

        if self.is_edit_worker:
            if not self.user.school.send_sms_edit_worker:
                return {'status': FAILED, 'result': "Sms xizmati o'chirilgan!"}

        if self.is_attendance:
            if not self.user.school.send_sms_attendance:
                return {'status': FAILED, 'result': "Sms xizmati o'chirilgan!"}

        if self.is_rating:
            if not self.user.school.send_sms_rating:
                return {'status': FAILED, 'result': "Sms xizmati o'chirilgan!"}

        if self.is_payment:
            if not self.user.school.send_sms_payment:
                return {'status': FAILED, 'result': "Sms xizmati o'chirilgan!"}

        if not len(str(self.phone)) == 9:
            return {'status': FAILED, 'result': "Tel raqam kirtishda xatolik!"}

        if not any([self.is_add_pupil, self.is_edit_pupil, self.is_add_worker, self.is_edit_worker, self.is_attendance,
                    self.is_rating, self.is_payment]):
            if self.message == '' or self.message == None:
                return {'status': FAILED, 'result': "Xabar matni kiritilmagan!"}
            else:
                self.message = self.clean_message(self.message)
        return {'status': SUCCESS, 'result': None}

    def send_message(self, message):
        try:
            URL = os.getenv('PLAY_MOBILE_URL')
            headers = {'Content-type': 'application/json'}
            payload = {
                "messages": [
                    {
                        "recipient": "998" + str(self.phone),
                        "message-id": str(self.message_id),
                        "sms": {
                            "originator": "3700",
                            "content": {
                                "text": str(message),
                            }
                        }
                    }
                ]
            }

            r = requests.post(URL, json=payload, headers=headers,
                              auth=(self.username, self.password))

            if self.is_add_pupil:
                self.user.school.add_pupil_sms_count -= 1
            else:
                self.user.school.sms_count -= self.spend
            self.user.school.save()


            from user.models import Sms
            sms = Sms.objects.create(school=self.user.school, sms_id=self.message_id, sms_count=self.spend,
                                   text=self.message,
                                   phone=self.phone)


            if not r.status_code == SUCCESS:
                sms.status = FAILED
                sms.save()
                return {'status': FAILED, 'result': "Sms xizmati tomonidan xatolik yuz berganligi sababli sms jo'natilmadi!"}

            sms.status = SUCCESS
            sms.save()
            return {'status': SUCCESS, 'result': "Sms muvaffaqiyatli jo'natildi!"}

        except Exception as e:
            send_message_to_developer(f"sms object create error: {e}")
            return {'status': FAILED, 'result': "Sms xizmatida tomonidan xatolik yuz berdi!"}

    def clean_message(self, message):
        message = message.replace('??', 'ts').replace('??', 'ch').replace('??',
                                                                        'yu').replace(
            '??', 'a').replace('??', 'b').replace('??', "q").replace('??', "o'").replace('??', "g'").replace('??',
                                                                                                        "h").replace(
            '??',
            "x").replace(
            '??', 'v').replace('??', 'g').replace('??', 'd').replace('??',
                                                                  'e').replace(
            '??', 'yo').replace('??', 'j').replace('??', 'z').replace('??', 'i').replace('??', 'y').replace('??',
                                                                                                       'k').replace(
            '??', 'l').replace('??', 'm').replace('??', 'n').replace('??', 'o').replace('??', 'p').replace('??',
                                                                                                      'r').replace(
            '??', 's').replace('??', 't').replace('??', 'u').replace('??', 'sh').replace('??', 'sh').replace('??',
                                                                                                        'f').replace(
            '??', 'e').replace('??', 'i').replace('??', 'ya').replace('??', "o'").replace('??', "'").replace('??',
                                                                                                        "'").replace(
            '???', "'").replace('???', '"').replace('???', '"').replace(',', ',').replace('.', '.').replace(':', ':')
        # filter upper
        message = message.replace('??', 'Ts').replace('??', 'Ch').replace('??', 'Yu').replace(
            '??', 'A').replace('??', 'B').replace('??', "Q").replace('??', "G'").replace('??', "H").replace('??',
                                                                                                       "X").replace(
            '??', 'V').replace('??', 'G').replace('??', 'D').replace('??',
                                                                  'E').replace(
            '??', 'Yo').replace('??', 'J').replace('??', 'Z').replace('??', 'I').replace('??', 'Y').replace('??',
                                                                                                       'K').replace(
            '??', 'L').replace('??', 'M').replace('??', 'N').replace('??', 'O').replace('??', 'P').replace('??',
                                                                                                      'R').replace(
            '??', 'S').replace('??', 'T').replace('??', 'U').replace('??', 'Sh').replace('??', 'Sh').replace('??',
                                                                                                        'F').replace(
            '??', 'E').replace('??', 'Ya')
        return message

    def make_messages(self):
        if self.is_add_pupil:
            self.message = f"Hurmatli {self.user.name}! Siz {self.user.group.category}-{self.user.group.number} guruhiga o'qishga qabul qilindingiz. Videodarslarni ko'rish va imtihon testlariga tayyorlanish uchun http://onless.uz/kirish manziliga kiring. \nLogin: {self.user.username}\nParol: {self.user.turbo}\nQo'shimcha ma'lumot uchun:{self.user.school.phone}"
            return self.message
        elif self.is_edit_pupil:
            self.message = f"Hurmatli {self.user.name}! Sizning ma'lumotlaringiz tahrirlandi. http://onless.uz/kirish manziliga kiring. \nLogin: {self.user.username}\nParol: {self.user.turbo}\nQo'shimcha ma'lumot uchun:{self.user.school.phone}"
            return self.message
        elif self.is_add_worker:
            if self.user.role == '6':
                role = 'instruktor'
            elif self.user.role == '5':
                role = 'hisobchi'
            else:
                role = "o'qituvchi"

            self.message = f"Hurmatli {self.user.name}! Siz {self.user.school.title} da {role} lavozimida ro'yhatga olindingiz. http://onless.uz/kirish manziliga kiring. \nLogin: {self.user.username}\nParol: {self.user.turbo}\nQo'shimcha ma'lumot uchun:{self.user.school.phone}"
            return self.message
        elif self.is_edit_worker:
            self.message = f"Hurmatli {self.user.name}! Sizning ma'lumotlaringiz tahrirlandi. http://onless.uz/kirish manziliga kiring. \nLogin: {self.user.username}\nParol: {self.user.turbo}\nQo'shimcha ma'lumot uchun:{self.user.school.phone}"
            return self.message
        elif self.is_attendance:
            if self.subject:
                self.message = f"Hurmatli {self.user.name}! Bugun {self.subject.short_title} fanidan darsga qatnashmadingiz. Bu hol qayta takrorlansa guruh ro'yhatidan chetlashtirilasiz!\nQo'shimcha ma'lumot uchun:{self.user.school.phone}"
                return self.message
        elif self.is_rating:
            if self.subject and self.score:
                self.message = f"Hurmatli {self.user.name}! Bugun {self.subject.short_title} fanidan {self.score} bahosini oldingiz!\nQo'shimcha ma'lumot uchun:{self.user.school.phone}"
                return self.message
        elif self.is_payment:
            if self.pay and self.payment:
                self.message = f"Hurmatli {self.user.name}! Avtomaktabga {self.pay} so???m to???lov qildingiz! Jami to???lovingiz {self.payment} so???m. Toifa bo???yicha {self.user.group.price - int(self.payment)} so???m qarzdorligingiz qoldi!\nQo'shimcha ma'lumot uchun:{self.user.school.phone}"
                return self.message
        else:
            return self.message

    def calculation_send_sms(self, message):
        try:
            length = len(message)
            if length:
                if length >= 0 and length <= 160:
                    self.spend = 1
                elif length > 160 and length <= 306:
                    self.spend = 2
                elif length > 306 and length <= 459:
                    self.spend = 3
                elif length > 459 and length <= 612:
                    self.spend = 4
                elif length > 612 and length <= 765:
                    self.spend = 5
                elif length > 765 and length <= 918:
                    self.spend = 6
                elif length > 918 and length <= 1071:
                    self.spend = 7
                elif length > 1071 and length <= 1224:
                    self.spend = 8
                else:
                    self.spend = 30

                if self.is_add_pupil:
                    if self.user.school.add_pupil_sms_count > 0:
                        return {'status': SUCCESS, 'result': None}
                    else:
                        return {'status': FAILED, 'result': "Hisobingizda kiritish sms mavjud emas!"}
                else:
                    if self.user.school.sms_count >= self.spend:
                        return {'status': SUCCESS, 'result': None}
                    else:
                        return {'status': FAILED, 'result': "Hisobingizda sms mavjud emas!"}
            else:
                return {'status': FAILED, 'result': "Xabar matni kiritilmagan!"}
        except:
            return {'status': FAILED, 'result': "Xatolik yuz berdi!"}
