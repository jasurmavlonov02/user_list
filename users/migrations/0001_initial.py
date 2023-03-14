# Generated by Django 4.1.7 on 2023-03-11 22:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=9, validators=[django.core.validators.RegexValidator(re.compile('^-?\\d+\\Z'), code='invalid', message='Enter a valid integer.')])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images/')),
                ('medical_examination_date', models.DateTimeField(blank=True, null=True)),
                ('otpusk', models.DateTimeField(blank=True, null=True)),
                ('zavod_dopusk', models.CharField(choices=[('NMZ', 'Nmz'), ('GMZ', 'Gmz'), ('SHMZ', 'Shmz')], max_length=25)),
                ('birth_day', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.category')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
