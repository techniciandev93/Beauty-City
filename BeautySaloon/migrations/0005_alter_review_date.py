# Generated by Django 5.0.1 on 2024-01-27 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BeautySaloon', '0004_alter_review_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата отзыва'),
        ),
    ]
