import phonenumbers
from django import forms


class PhoneNumberForm(forms.Form):
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


class VerificationCodeForm(forms.Form):
    phone_number = forms.CharField(required=True)

    digit1 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(
            attrs={'pattern': '[0-9]', 'class': 'tipsPopup__form_inputNum popup__input digit-input', 'maxlength': '1'})
    )
    digit2 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(
            attrs={'pattern': '[0-9]', 'class': 'tipsPopup__form_inputNum popup__input digit-input', 'maxlength': '1'})
    )
    digit3 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(
            attrs={'pattern': '[0-9]', 'class': 'tipsPopup__form_inputNum popup__input digit-input', 'maxlength': '1'})
    )
    digit4 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(
            attrs={'pattern': '[0-9]', 'class': 'tipsPopup__form_inputNum popup__input digit-input', 'maxlength': '1'})
    )
