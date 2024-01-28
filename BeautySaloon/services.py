from django.db.models import Sum
from django.utils import timezone

from BeautySaloon.models import Order
from users.models import CustomUser


def monthly_payment_stats():
    current_month = timezone.now().month
    total_payment_this_month = Order.objects.filter(
        appointment_time__month=current_month,
        payment_state=True
    ).aggregate(total_payment=Sum('price'))['total_payment']
    total_payment_this_month = total_payment_this_month if total_payment_this_month is not None else 0
    return total_payment_this_month


def registered_users_stats():
    current_year = timezone.now().year
    current_month = timezone.now().month
    users_registered_this_month = CustomUser.objects.filter(date_joined__month=current_month).count()
    total_users_registered_this_year = CustomUser.objects.filter(date_joined__year=current_year).count()
    total_users = CustomUser.objects.count()
    return users_registered_this_month, total_users_registered_this_year, total_users
