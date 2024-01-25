from django.shortcuts import render

from users.forms import VerificationCodeForm


def index(request):
    form = VerificationCodeForm()
    return render(request, 'BeautySaloon/index.html', {'form': form})



