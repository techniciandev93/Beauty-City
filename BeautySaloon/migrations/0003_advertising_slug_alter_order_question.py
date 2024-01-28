# Generated by Django 5.0.1 on 2024-01-28 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BeautySaloon', '0002_order_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertising',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True, unique=True, verbose_name='Уникальная часть url'),
        ),
        migrations.AlterField(
            model_name='order',
            name='question',
            field=models.TextField(blank=True, default=None, verbose_name='Вопрос к заказу'),
        ),
    ]
