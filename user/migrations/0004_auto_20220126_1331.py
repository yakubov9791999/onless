# Generated by Django 3.0.6 on 2022-01-26 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_rating_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='year',
            field=models.IntegerField(default=2022, null=True, verbose_name="O'quv yili"),
        ),
    ]