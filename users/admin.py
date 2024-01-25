from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('phone_number', 'username', 'email', 'is_staff')
    search_fields = ('phone_number', 'username', 'email')

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные данные', {'fields': ('phone_number', 'code')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'username', 'password1', 'password2'),
        }),
    )
