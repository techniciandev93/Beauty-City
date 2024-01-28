from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import Review


class ReviewTextForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']


class OrderForm(forms.Form):
    fname = forms.CharField(
        label='Имя клиента',
        max_length=200,
        required=True
    )
    tel = PhoneNumberField()
