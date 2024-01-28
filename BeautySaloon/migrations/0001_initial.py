# Generated by Django 5.0.1 on 2024-01-27 11:58

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertising',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=200, verbose_name='Рекламное место')),
                ('adv_counter', models.IntegerField(default=0, verbose_name='Счетчик переходов')),
            ],
            options={
                'verbose_name': 'Реклама',
                'verbose_name_plural': 'Реклама',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование услуги')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(1)], verbose_name='цена')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Фото услуги')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категория сервиса',
                'verbose_name_plural': 'Категории сервиса',
            },
        ),
        migrations.CreateModel(
            name='Saloon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название салона')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Фото салона')),
                ('service', models.ManyToManyField(related_name='saloons', to='BeautySaloon.service', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Салон',
                'verbose_name_plural': 'Салоны',
            },
        ),
        migrations.AddField(
            model_name='service',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='services', to='BeautySaloon.servicecategory', verbose_name='Категория сервиса'),
        ),
        migrations.CreateModel(
            name='Specialist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя мастера')),
                ('speciality', models.CharField(max_length=200, verbose_name='Специальность')),
                ('career_start', models.DateField(blank=True, null=True, verbose_name='Старт карьеры')),
                ('start_work_time', models.TimeField(verbose_name='Время начала работы')),
                ('end_work_time', models.TimeField(verbose_name='Время окончания работы')),
                ('image', models.ImageField(upload_to='images/', verbose_name='Фото специалиста')),
                ('saloon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specialists', to='BeautySaloon.saloon', verbose_name='Салон')),
                ('service', models.ManyToManyField(related_name='specialists', to='BeautySaloon.service', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Мастер',
                'verbose_name_plural': 'Мастера',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст отзыва')),
                ('rating', models.CharField(blank=True, choices=[('one star', '1'), ('two_stars', '2'), ('three_stars', '3'), ('four_stars', '4'), ('five_stars', '5')], db_index=True, max_length=50, null=True, verbose_name='Рейтинг специалиста')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Дата отзыва')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='BeautySaloon.specialist', verbose_name='Специалист')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_time', models.DateTimeField(verbose_name='Время записи')),
                ('end_appointment_time', models.DateTimeField(blank=True, null=True, verbose_name='Конец времени записи')),
                ('payment_state', models.BooleanField(default=False, verbose_name='Статус оплаты')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Итоговая сумма заказа')),
                ('tip', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Чаевые')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
                ('saloon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='BeautySaloon.saloon', verbose_name='Салон')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='BeautySaloon.service', verbose_name='Услуга')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='BeautySaloon.specialist', verbose_name='Специалист')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
