from django.contrib import admin

from BeautySaloon.models import SmsVerificationCode


@admin.register(SmsVerificationCode)
class WareHouseAdmin(admin.ModelAdmin):
    pass
