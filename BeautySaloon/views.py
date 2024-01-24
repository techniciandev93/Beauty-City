from django.shortcuts import render, redirect
from django.views import View

from BeautySaloon.forms import VerificationCodeForm
from BeautySaloon.services import generate_or_update_verification_code


def index(request):
    form = VerificationCodeForm()
    return render(request, 'BeautySaloon/index.html', {'form': form})


class SmsAuthorizationView(View):
    template_name = 'BeautySaloon/login.html'

    def get(self, request, *args, **kwargs):
        form = VerificationCodeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            generate_or_update_verification_code(phone_number)
            return redirect('index')
        else:
            return render(request, self.template_name, {'form': form})
