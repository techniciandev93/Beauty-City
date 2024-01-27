# Generated by Django 5.0.1 on 2024-01-27 16:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BeautySaloon', '0002_alter_order_tip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specialist',
            name='service',
        ),
        migrations.AddField(
            model_name='order',
            name='review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='BeautySaloon.review', verbose_name='Отзыв'),
        ),
        migrations.AddField(
            model_name='specialist',
            name='service_category',
            field=models.ManyToManyField(related_name='specialists', to='BeautySaloon.servicecategory', verbose_name='Категория оказываемых услуг'),
        ),
    ]
