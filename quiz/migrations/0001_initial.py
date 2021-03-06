# Generated by Django 3.0.6 on 2021-12-14 14:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import quiz.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=600)),
                ('is_true', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allowed', quiz.fields.IntegerRangeField(default=2, verbose_name='Ruxsat berilgan urinishlar')),
                ('solved', quiz.fields.IntegerRangeField(default=0, verbose_name='Bajarilgan urinishlar')),
            ],
            options={
                'verbose_name': 'Urinish',
                'verbose_name_plural': 'Urinishlar',
            },
        ),
        migrations.CreateModel(
            name='Bilet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CheckTestColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Javob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_uz', models.CharField(blank=True, max_length=1000)),
                ('text_kr', models.CharField(blank=True, max_length=1000)),
                ('text_ru', models.CharField(blank=True, max_length=1000)),
                ('is_true', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Test javobi',
                'verbose_name_plural': 'Test javoblari',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=600)),
                ('img', models.ImageField(blank=True, default='', upload_to='quiz/img/%Y-%m-%d/')),
                ('is_active', models.BooleanField(default=True)),
                ('is_test', models.BooleanField(default=False)),
                ('pub_date', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name': 'Test natijasi',
                'verbose_name_plural': 'Test natijalari',
            },
        ),
        migrations.CreateModel(
            name='ResultJavob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('j_1', models.BooleanField(default=False)),
                ('j_2', models.BooleanField(default=False)),
                ('j_3', models.BooleanField(default=False)),
                ('j_4', models.BooleanField(default=False)),
                ('j_5', models.BooleanField(default=False)),
                ('j_6', models.BooleanField(default=False)),
                ('j_7', models.BooleanField(default=False)),
                ('j_8', models.BooleanField(default=False)),
                ('j_9', models.BooleanField(default=False)),
                ('j_10', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ResultQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_last', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Eski natija',
                'verbose_name_plural': 'Eski natijalar',
            },
        ),
        migrations.CreateModel(
            name='Savol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bilet_savol', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=2)),
                ('title_uz', models.CharField(blank=True, max_length=1000)),
                ('title_kr', models.CharField(blank=True, max_length=1000)),
                ('title_ru', models.CharField(blank=True, max_length=1000)),
                ('photo', models.ImageField(blank=True, default='', upload_to='quiz/img/')),
                ('is_photo', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('comment', models.TextField(blank=True)),
                ('bilet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='quiz.Bilet')),
            ],
            options={
                'verbose_name': 'Test savoli',
                'verbose_name_plural': 'Test savollari',
            },
        ),
    ]
