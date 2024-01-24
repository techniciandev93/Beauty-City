import phonenumbers
from django import forms


class VerificationCodeForm(forms.Form):
    phone_number = forms.CharField(
        label='Номер телефона',
        widget=forms.TextInput(attrs={'placeholder': '+7(999)999--99-99', 'class': 'contacts__form_iunput'}),
        required=True,
    )
    agree_to_policy = forms.BooleanField(
        label='Я согласен(а) с политикой конфиденциальности',
        widget=forms.CheckboxInput(attrs={'class': 'contacts__form_checkbox'}),
        required=True,
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        try:
            parsed_phone_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_phone_number):
                raise forms.ValidationError('Неверный формат номера телефона.')
        except phonenumbers.NumberParseException:
            raise forms.ValidationError('Ошибка при разборе номера телефона.')
        return phone_number
