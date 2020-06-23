# Generated by Django 3.0.6 on 2020-06-23 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0002_schedule_subject'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schedule',
            options={'verbose_name': 'Dars jadvali', 'verbose_name_plural': 'Dars jadvallari'},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'verbose_name': 'Fan', 'verbose_name_plural': 'Fanlar'},
        ),
        migrations.AlterField(
            model_name='subject',
            name='category',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('BC', 'BC'), ('C', 'C'), ('D', 'D'), ('E', 'E')], default='A', max_length=3),
        ),
    ]
