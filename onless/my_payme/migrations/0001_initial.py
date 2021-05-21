# Generated by Django 3.0.6 on 2021-05-14 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_id', models.CharField(max_length=255)),
                ('request_id', models.IntegerField()),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('account', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[(0, 'processing'), (1, 'paid'), (2, 'failed')], default=0, max_length=10)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('pay_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
