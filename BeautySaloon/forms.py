from django import forms


class VerificationCodeForm(forms.Form):
    phone_number = forms.CharField(
        label='Номер телефона',
        widget=forms.TextInput(attrs={'placeholder': '+7(999)999--99-99'}),
        required=True,
    )
    agree_to_policy = forms.BooleanField(
        label='Я согласен(а) с политикой конфиденциальности',
        required=True,
    )
