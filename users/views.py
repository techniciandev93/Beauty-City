from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View

from users.forms import PhoneNumberForm, VerificationCodeForm
from users.models import CustomUser
from users.services import generate_or_update_verification_code


class SmsAuthorizationView(View):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        form = PhoneNumberForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            generate_or_update_verification_code(phone_number)

            code_form = VerificationCodeForm()
            return render(request, 'users/confirmation_number.html', {
                'phone_number': phone_number,
                'form': code_form})
        else:
            return render(request, self.template_name, {'form': form})


class ConfirmationNumberView(View):
    template_name = 'users/confirmation_number.html'

    def post(self, request, *args, **kwargs):
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            digit1 = form.cleaned_data['digit1']
            digit2 = form.cleaned_data['digit2']
            digit3 = form.cleaned_data['digit3']
            digit4 = form.cleaned_data['digit4']
            phone_number = form.cleaned_data['phone_number']

            code = int(''.join([digit1, digit2, digit3, digit4]))
            user_exists = CustomUser.objects.filter(phone_number=phone_number, code=code).exists()

            if user_exists:
                user_instance = CustomUser.objects.get(phone_number=phone_number, code=code)
                user_instance.code = None
                user_instance.save()
                login(request, user_instance)
                return redirect('index')
            return render(request, self.template_name, {''
                                                        'form': form,
                                                        'phone_number': phone_number,
                                                        'sms_error': 'Неверный код'})
        else:
            return render(request, self.template_name, {'form': form})
