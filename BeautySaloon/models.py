from datetime import datetime

from users.models import CustomUser
from django.core.validators import MinValueValidator
from django.db import models


class Saloon(models.Model):
    name = models.CharField(verbose_name='Название салона', max_length=200)
    address = models.CharField(verbose_name='Адрес', max_length=200)
    service = models.ManyToManyField(
        'Service',
        verbose_name='Услуга',
        related_name='saloons')
    image = models.ImageField(verbose_name='Фото салона', upload_to='images/')

    class Meta:
        verbose_name = 'Салон'
        verbose_name_plural = 'Салоны'

    def __str__(self):
        return f'Салон {self.name}'


class Service(models.Model):
    name = models.CharField(verbose_name='Наименование услуги', max_length=200)
    price = models.DecimalField(verbose_name='цена', max_digits=8, decimal_places=2, validators=[MinValueValidator(1)])
    image = models.ImageField(verbose_name='Фото услуги', upload_to='images/')
    category = models.ForeignKey(
        'ServiceCategory',
        verbose_name='Категория сервиса',
        on_delete=models.CASCADE,
        related_name='services',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return f'Услуга {self.name}'


class Specialist(models.Model):
    name = models.CharField(verbose_name='Имя мастера', max_length=200)
    speciality = models.CharField(verbose_name='Специальность', max_length=200)
    career_start = models.DateField(verbose_name='Старт карьеры', null=True, blank=True)
    start_work_time = models.TimeField(verbose_name='Время начала работы')
    end_work_time = models.TimeField(verbose_name='Время окончания работы')
    service = models.ManyToManyField(
        'Service',
        verbose_name='Услуга',
        related_name='specialists')
    image = models.ImageField(verbose_name='Фото специалиста', upload_to='images/')
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE, verbose_name='Салон', related_name='specialists')

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    def __str__(self):
        return f'Мастер {self.name}'

    def experience(self):
        today = datetime.today().date()
        delta = today - self.career_start
        years = delta.days // 365
        months = (delta.days % 365) // 30
        return years, months


class Order(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Клиент', related_name='orders')
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE, verbose_name='Салон', related_name='orders')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга', related_name='orders')
    specialist = models.ForeignKey('Specialist',
                                   on_delete=models.CASCADE,
                                   verbose_name='Специалист',
                                   related_name='orders')
    appointment_time = models.DateTimeField(verbose_name='Время записи')
    end_appointment_time = models.DateTimeField(verbose_name='Конец времени записи', blank=True, null=True)
    payment_state = models.BooleanField(verbose_name='Статус оплаты', default=False)
    price = models.DecimalField(
        verbose_name='Итоговая сумма заказа',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    tip = models.DecimalField(
        verbose_name='Чаевые',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1)], blank=True, null=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'ID заказа {self.id}'


class Advertising(models.Model):
    place = models.CharField(verbose_name='Рекламное место', max_length=200)
    adv_counter = models.IntegerField(verbose_name='Счетчик переходов', default=0)

    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Реклама'

    def __int__(self):
        return f'Рекламное место {self.place}'


class Review(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Клиент', related_name='reviews')
    specialist = models.ForeignKey('Specialist',
                                   on_delete=models.CASCADE,
                                   verbose_name='Специалист',
                                   related_name='reviews')
    text = models.TextField(verbose_name='Текст отзыва', blank=True, null=True)
    RATING_CHOICES = [
        ('one star', '1'),
        ('two_stars', '2'),
        ('three_stars', '3'),
        ('four_stars', '4'),
        ('five_stars', '5'),
    ]
    rating = models.CharField(
        verbose_name='Рейтинг специалиста',
        max_length=50,
        choices=RATING_CHOICES,
        blank=True,
        null=True,
        db_index=True)

    date = models.DateField(verbose_name='Дата отзыва', blank=True, null=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'ID отзыва {self.id}'


class ServiceCategory(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=200)

    class Meta:
        verbose_name = 'Категория сервиса'
        verbose_name_plural = 'Категории сервиса'

    def __str__(self):
        return self.name
