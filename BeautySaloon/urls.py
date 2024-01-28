from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('select_saloon/', views.get_saloons, name='saloon'),
    path('select_service/', views.get_services, name='select_services'),
    path('select_master/', views.get_masters, name='select_master'),
    path('select_date/', views.get_date, name='select_date'),
    path('select_time/', views.get_time, name='select_time'),
    path('create_order/', views.create_order, name='create_order'),
    path('profile/', views.profile, name='profile'),
    path('review/<int:order_id>/', views.create_review, name='review'),
    path('advertising/<slug:slug>/', views.advertising, name='advertising_detail'),
]
