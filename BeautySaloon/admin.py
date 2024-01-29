import shortuuid
from django.contrib import admin
from django.utils.html import format_html

from BeautySaloon.models import Saloon, Service, Specialist, Review, ServiceCategory, Order, Advertising, \
    ConsultationRequest


@admin.register(Saloon)
class SaloonAdmin(admin.ModelAdmin):
    fields = ['name', 'address', 'service', 'image']
    raw_id_fields = ['service']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    fields = ['name', 'price', 'category', 'image']
    raw_id_fields = ['category']


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    fields = ['saloon', 'name', 'career_start', 'speciality',
              'start_work_time', 'end_work_time', 'service_category', 'image']
    raw_id_fields = ['service_category', 'saloon']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
    fields = ['client', 'specialist', 'text', 'rating', 'date']
    raw_id_fields = ['client', 'specialist']


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['id', 'client', 'saloon', 'service', 'specialist', 'appointment_time', 'price', 'tip',
                    'payment_state', 'question']


@admin.register(Advertising)
class AdvertisingAdmin(admin.ModelAdmin):
    readonly_fields = ('get_absolute_url',)
    list_display = ('place', 'adv_counter', 'slug', 'get_absolute_url')
    prepopulated_fields = {'slug': ('place',)}

    def save_model(self, request, obj, form, change):
        if not change:
            obj.slug = shortuuid.uuid()
        super().save_model(request, obj, form, change)


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
    list_display = ('name', 'phone_number', 'question', 'date')
    search_fields = ('name', 'phone_number', 'question')
    list_filter = ('date',)
