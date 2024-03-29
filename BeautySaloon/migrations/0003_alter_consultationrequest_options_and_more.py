# Generated by Django 5.0.1 on 2024-01-29 12:08

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BeautySaloon', '0002_consultationrequest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consultationrequest',
            options={'verbose_name': 'Консультация', 'verbose_name_plural': 'Консультации'},
        ),
        migrations.AlterField(
            model_name='consultationrequest',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='consultationrequest',
            name='question',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Вопрос'),
        ),
    ]
