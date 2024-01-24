# Generated by Django 5.0.1 on 2024-01-24 14:10

import django.core.validators
import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsVerificationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(validators=[django.core.validators.MaxValueValidator(9999, message='Код должен быть 4-значным числом'), django.core.validators.MinValueValidator(1000, message='Код должен быть 4-значным числом')], verbose_name='Код подтверждения')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Мобильный номер')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления кода')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Sms-код для подтверждения',
                'verbose_name_plural': 'Sms-коды для подтверждения',
            },
        ),
    ]