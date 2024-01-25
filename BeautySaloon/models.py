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


class Saloon(models.Model):
    address = models.CharField(verbose_name='Адрес', max_length=200)
    service = models.ForeignKey(
        'Service',
        on_delete=models.SET_NULL,
        verbose_name='Услуга',
        related_name='saloons')
    specialist = models.ForeignKey(
        'Specialist',
        on_delete=models.SET_NULL,
        verbose_name='Специалист',
        related_name='saloons')

    class Meta:
        verbose_name = 'Салон'
        verbose_name_plural = 'Салоны'

    def __str__(self):
        return f'Салон по адресу {self.address}'


class Service(models.Model):
    name = models.CharField(verbose_name='Наименование услуги', max_length=200)
    specialist = models.ForeignKey('Specialist',
                                   on_delete=models.SET_NULL,
                                   verbose_name='Специалист',
                                   related_name='services')
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2, validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return f'Услуга {self.name}'


class Specialist(models.Model):
    name = models.CharField(verbose_name='Имя мастера', max_length=200)
    start_work_time = models.TimeField(verbose_name='Время начала работы')
    end_work_time = models.TimeField(verbose_name='Время окончания работы')
    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        verbose_name='Услуга',
        related_name='specialists')

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    def __str__(self):
        return f'Мастер {self.name}'


class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент', related_name='orders')
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE, verbose_name='Салон', related_name='orders')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга', related_name='orders')
    appointment_time = models.DateTimeField(verbose_name='Время записи')
    payment_state = models.BooleanField(verbose_name='Статус оплаты', default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'ID заказа {self.id}'
