# Generated by Django 3.0.6 on 2021-12-14 14:50

from django.db import migrations, models
import django.utils.timezone
import sign.models
import sign.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('sort', models.IntegerField(default=1)),
                ('file', models.FileField(upload_to=sign.models.path_and_rename, validators=[sign.validators.validate_file_extension])),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materiallar',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('date', models.DateField(blank=True, null=True, verbose_name='Kuni')),
                ('lesson_time', models.SmallIntegerField(default=2)),
                ('is_active', models.BooleanField(default=True)),
                ('theme_order', models.CharField(blank=True, max_length=5, null=True, verbose_name='Mavzu tartibi')),
                ('sort', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name': 'Dars jadvali',
                'verbose_name_plural': 'Dars jadvallari',
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='Sign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('text', models.CharField(blank=True, max_length=5000)),
                ('photo', models.ImageField(upload_to='sign/')),
                ('sort', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='SignCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('sort', models.IntegerField(default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_title', models.CharField(max_length=600, verbose_name='Qisqa nomi')),
                ('long_title', models.TextField(verbose_name="To'liq nomi")),
                ('sort', models.IntegerField(blank=True, null=True, verbose_name='Tartibi')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Fan',
                'verbose_name_plural': 'Fanlar',
                'ordering': ['sort'],
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='Nomi')),
                ('sort', models.SmallIntegerField(default=1, verbose_name='Tartibi')),
                ('theme_order', models.CharField(blank=True, max_length=5, null=True, verbose_name='Mavzu tartibi')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('lesson_time', models.SmallIntegerField(default=2)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Mavzu',
                'verbose_name_plural': 'Mavzular',
                'ordering': ['sort'],
            },
        ),
    ]
