from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Поле phone_number обязательно для заполнения')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(verbose_name='Мобильный номер', unique=True, blank=False)
    username = models.CharField(verbose_name='Логин', max_length=150, blank=True)
    code = models.IntegerField(verbose_name='Код подтверждения', blank=True, null=True,
                               validators=[
                                   MaxValueValidator(9999, message='Код должен быть 4-значным числом'),
                                   MinValueValidator(1000, message='Код должен быть 4-значным числом'),
                               ]
                               )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.phone_number} {self.username}'

    @property
    def calculate_total_unpaid_orders(self):
        total_unpaid_orders = self.orders.filter(payment_state=False).aggregate(total=Sum('service__price'))['total']
        return total_unpaid_orders if total_unpaid_orders is not None else 0
