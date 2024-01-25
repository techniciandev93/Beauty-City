from django.urls import path
from .views import SmsAuthorizationView, ConfirmationNumberView

app_name = 'users'

urlpatterns = [
    path('', SmsAuthorizationView.as_view(), name='login'),
    path('verification-code/', ConfirmationNumberView.as_view(), name='verification_code')
]
