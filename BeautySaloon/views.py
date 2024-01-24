from django.shortcuts import render, redirect

from BeautySaloon.forms import VerificationCodeForm
from BeautySaloon.services import verification_code


def index(request):
    form = VerificationCodeForm()
    return render(request, 'BeautySaloon/index.html', {'form': form})


def sms_authorization(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            #verification_code(phone_number)
            return None
        else:
            return render(request, 'BeautySaloon/index.html', {'form': form})
