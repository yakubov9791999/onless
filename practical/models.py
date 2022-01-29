from django.db import models
from user.models import *


# # Create your models here.

class CarModel(models.Model):
    title = models.CharField("Model nomi", max_length=30)
    is_nationality = models.BooleanField("Milliyligi", default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Avtomobil modeli"
        verbose_name_plural = "Avtomobil modellari"


class Car(models.Model):
    model = models.ForeignKey(CarModel, verbose_name="Avtomobil modeli", on_delete=models.CASCADE)
    region = models.ForeignKey(Region, verbose_name="Viloyatni tanlang", on_delete=models.CASCADE, null=True)
    state_number = models.CharField("Davlat raqam belgisi", max_length=255)
    instructor = models.ForeignKey(User, verbose_name="Instruktor", on_delete=models.CASCADE, null=True)
    is_rental = models.BooleanField(default=False,
                                    verbose_name="Ijara avtomobil")  # agarda avtomobil ijara shartnoma asosida olingan bo'lsa
    price = models.IntegerField("Avtomobil narxi")

    class Meta:
        verbose_name_plural = 'Avtomobillar'
        verbose_name = 'Avtomobil'


BY_WHOM = (
    ("1", "Instruktor"),
    ("2", "O'quvchi"),
)


class Practical(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="O'qituvchi",
                                   related_name='practical_instructor')
    pupil = models.ForeignKey(User, verbose_name="O'quvchi", null=True, on_delete=models.CASCADE,
                              related_name='practical_pupil')
    created_date = models.DateTimeField(default=timezone.now)
    training_time = models.DateTimeField("Amaliy mashg'ulotga yozilgan vaqti")
    status = models.BooleanField("Amaliy mashg'ulot holati", default=True)
    cancel = models.BooleanField("Bekor qilinganligi", default=False)
    reason_for_cancel = models.CharField("Amaliy mashg'ulotni bekor qilish sababi", max_length=255)
    by_whom = models.CharField("Kim tomonidan bekor qilinganligi", choices=BY_WHOM, max_length=255)
    is_partnership = models.BooleanField("Sherik bilan",
                                         default=True)  # Ayrim o'quvchilar dugonasi, opasi bilan birga chiadi. SHunday ekan ular o'zaro kelishga holda bitta instruktorga bir vaqtda yozdira oladi.
    is_payment = models.BooleanField("To'lov to'langanligi", default=False)  # To'lov to'langanligi
    is_prepaid = models.BooleanField("To'lov avvaldan", default=True)  # Avvaldan to'lov qabul qilinishi kerak bo'lsa
    is_postpaid = models.BooleanField("To'lov bajarilganidan so'ng",
                                      default=False)  # Bajarilganidan so'ng to'lov qilinishi kerak bo'lsa
    is_bonus = models.BooleanField("Bonus", default=False)
    is_bonus_comment = models.TextField("Qanday turdagi bonus")
    done = models.BooleanField("Bajarildi", default=False)

    class Meta:
        verbose_name_plural = "Amaliy mashg'ulotlar"
        verbose_name = "Amaliy mashg'ulot"


class DayOfWeek(models.Model):  # dam olish kunlari yoki instruktorni ishi chiqib qolsa biriktirib qo'yadi
    instruktor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='day_of_week_instruktor', null=True)
    day = models.DateField()

    class Meta:
        verbose_name = "Dam olish kuni"
        verbose_name_plural = "Dam olish kunlari"


class PaymentForPractical(models.Model):
    sum = models.IntegerField("To'lov summasi")
    created_date = models.DateTimeField(default=timezone.now)
    pupil = models.ForeignKey(User, verbose_name="O'quvchi", null=True, on_delete=models.CASCADE,
                              related_name='practical_payment_pupil')


    class Meta:
        verbose_name = "Vajdeniya uchun to'lov"
        verbose_name_plural = "Vajdeniya uchun to'lovlar"


