import random

from rest_framework import serializers

from user.decorators import get_pasport, get_name
from user.models import User


class CreatePupilSerializer(serializers.ModelSerializer):
    pasport = serializers.CharField(
        required=True,
        max_length=9,
        error_messages={
            "required": "Pasport to'ldirish majburiy!",
            "blank": "Pasport bo'sh bo'lmasligi kerak!",
            "max_length": "Pasport 9 tadan ortiq bo'lmasligi kerak!",
            "unique": "Bu pasport allaqachon ro'yhatdan o'tkazilgan!",
        },
    )
    phone = serializers.IntegerField(
        required=True,
        min_value=100000000,
        max_value=999999999,
        error_messages={
            "required": "Tel raqam to'ldirish majburiy!",
            "min_value": "Tel raqam 9 xonali sondan iborat bo'lishi kerak!",
            "max_value": "Tel raqam 9 xonali sondan iborat bo'lishi kerak!",
        })

    class Meta:
        model = User
        fields = [
            'id',
            'pasport',
            'name',
            'phone',
            'birthday',
        ]
        extra_kwargs = {
            'pasport': {'required': True},
            'name': {'required': True},
        }

    def validate_pasport(self, value):
        value = get_pasport(value)
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(value + " pasport allaqachon ro'yhatdan o'tkazilgan!")
        return value

    def validate_name(self, value):
        return get_name(value)

    def create(self, validated_data):
        password = random.randint(1000000, 9999999)
        validated_data['username'] = validated_data['pasport']
        instance = super().create(validated_data)
        instance.set_password(str(password))
        instance.turbo = str(password)
        instance.role = '4'
        instance.is_superuser = False
        instance.email = ''
        instance.school = self.context.get('request').user.school
        instance.group_id = self.context.get('group_id')
        instance.save()
        return instance
