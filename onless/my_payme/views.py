from django.shortcuts import render
from my_payme.models import Transaction
import requests
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from my_payme.serializers import SubscribeSerializer
from my_payme.config import *


# Create your views here.


class PaymentApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['params']['token']
        result = self.receipts_create(token, serializer.validated_data)
        return Response(result)

    def receipts_create(self, token, validated_data):
        print(validated_data)
        key_2 = validated_data['params']['account'][KEY_2] if KEY_2 else None
        data = dict(
            id=validated_data['id'],
            method='receipts.create',
            params=dict(
                amount=validated_data['params']['amount'],
                account=dict(
                    KEY_1=validated_data['params']['account'][KEY_1],
                    KEY_2=key_2,
                )
            )
        )
        print(AUTHORIZATION_PAY)
        response = requests.post(URL, json=data, headers=AUTHORIZATION_PAY)
        print('response', response)
        result = response.json()
        print(result)

        if 'error' in result:
            return result

        trans_id = result['result']['receipt']['_id']
        trans = Transaction()
        print(result)
        trans.create_transaction(
            trans_id=trans_id,
            request_id=result['id'],
            amount=result['result']['receipt']['amount'],
            account=result['result']['receipt']['account'],
            status=trans.PROCESS,
        )
        result = self.receipts_pay(trans_id, token)
        return result

    def receipts_pay(self, trans_id, token):
        data = dict(
            method='receipts.pay',
            params=dict(
                id=trans_id,
                token=token,
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION_PAY)
        result = response.json()
        trans = Transaction()

        if 'error' in result:
            trans.update_transaction(
                trans_id=trans_id,
                status=trans.FAILED,
            )
            return result

        trans.update_transaction(
            trans_id=result['result']['receipt']['_id'],
            status=trans.PAID,
        )

        return result


class CardCreateApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        result = self.card_create(serializer.validated_data)
        print('post : ', result)
        return Response(result)

    def card_create(self, validated_data):
        print('cart_create_validate :', validated_data)
        data = dict(
            id=validated_data['id'],
            method='cards.create',
            params=dict(
                card=dict(
                    number=validated_data['params']['card']['number'],
                    expire=validated_data['params']['card']['expire'],
                ),
                # amount=validated_data['params']['amount'],
                save=validated_data['params']['save']
            )
        )
        print('data', data)
        response = requests.post(URL, json=data, headers=AUTHORIZATION_CARD)
        result = response.json()
        if 'error' in result:
            return result

        token = result['result']['card']['token']
        result = self.card_get_verify_code(token)

        return result

    def card_get_verify_code(self, token):
        data = dict(
            method='cards.get_verify_code',
            params=dict(
                token=token
            )
        )

        print('verify code:', data)
        response = requests.post(URL, json=data, headers=AUTHORIZATION_CARD)
        result = response.json()
        if 'error' in result:
            return result

        result.update(token=token)
        print(result)
        return result


class CardVerifyApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        result = self.card_verify(serializer.validated_data)

        return Response(result)

    def card_verify(self, validated_data):
        data = dict(
            id=validated_data['id'],
            method='cards.verify',
            params=dict(
                token=validated_data['params']['token'],
                code=validated_data['params']['code']
            )
        )
        response = requests.post(URL, json=data, headers=AUTHORIZATION_CARD)
        result = response.json()

        return result
