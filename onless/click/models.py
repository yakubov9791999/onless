from django.db import models

from user.models import *


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order')
    created_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    is_paid = models.BooleanField(verbose_name='To\'langanligi',default=False)
    amount = models.CharField(max_length=20,verbose_name="Summasi")