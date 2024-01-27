from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from .views import SmsAuthorizationView, ConfirmationNumberView

app_name = 'users'

urlpatterns = [
    path('', SmsAuthorizationView.as_view(), name='login'),
    path('verification-code/', ConfirmationNumberView.as_view(), name='verification_code'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('index')), name='logout'),
]
