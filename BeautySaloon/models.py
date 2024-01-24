from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class SmsVerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
    code = models.IntegerField(verbose_name='Код подтверждения',
                               validators=[
                                   MaxValueValidator(9999, message='Код должен быть 4-значным числом'),
                                   MinValueValidator(1000, message='Код должен быть 4-значным числом'),
                               ]
                               )
    phone_number = PhoneNumberField(verbose_name='Мобильный номер')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления кода')

    class Meta:
        verbose_name = 'Sms-код для подтверждения'
        verbose_name_plural = 'Sms-коды для подтверждения'

    def __str__(self):
        return f'{self.phone_number}'
