# Generated by Django 3.0.6 on 2021-12-25 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practical', '0002_auto_20211214_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='price',
            field=models.IntegerField(verbose_name='Avtomobil narxi'),
        ),
        migrations.AlterField(
            model_name='paymentforpractical',
            name='sum',
            field=models.IntegerField(verbose_name="To'lov summasi"),
        ),
    ]