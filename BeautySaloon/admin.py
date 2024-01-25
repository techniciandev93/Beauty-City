from django.contrib import admin

from BeautySaloon.models import Saloon, Service, Specialist, Review


@admin.register(Saloon)
class SaloonAdmin(admin.ModelAdmin):
    fields = ['name', 'address', 'service', 'image']
    raw_id_fields = ['service']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    fields = ['name', 'price', 'image']


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    fields = ['saloon', 'name', 'career_start', 'speciality', 'start_work_time', 'end_work_time', 'service', 'image']
    raw_id_fields = ['service', 'saloon']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    fields = ['client', 'specialist', 'text', 'rating', 'date']
    raw_id_fields = ['client', 'specialist']
