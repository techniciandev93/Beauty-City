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


class ConsultationRequestForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'contacts__form_iunput',
                                                                         'placeholder': 'Введите имя'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'contacts__form_iunput',
                                                                                'placeholder': '+7(999)999--99-99'}))
    question = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Вопрос(необязательно)',
                                                            'class': 'contacts__form_textarea',
                                                            'rows': 4}), required=False)
    agree_to_privacy_policy = forms.BooleanField()

    def clean_agree_to_privacy_policy(self):
        agree_to_privacy_policy = self.cleaned_data.get('agree_to_privacy_policy')
        if not agree_to_privacy_policy:
            raise forms.ValidationError('Вы должны согласиться с политикой конфиденциальности.')
        return agree_to_privacy_policy
