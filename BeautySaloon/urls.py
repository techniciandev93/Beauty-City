from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('select_saloon/', views.get_saloons, name='saloon'),
    path('select_service/', views.get_services, name='select_services'),
    path('select_master/', views.get_masters, name='select_master'),
    path('profile/', views.profile, name='profile'),
    path('review/<int:order_id>/', views.create_review, name='review'),

]
