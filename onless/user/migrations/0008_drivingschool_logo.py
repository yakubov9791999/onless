# Generated by Django 3.0.6 on 2020-06-05 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20200605_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='drivingschool',
            name='logo',
            field=models.ImageField(default=1, upload_to='school/'),
            preserve_default=False,
        ),
    ]