import random

import requests

from BeautyCity.settings import SMS_RU_API_ID
from BeautySaloon.models import SmsVerificationCode


def send_sms(recipient_number, message):
    params = {'api_id': SMS_RU_API_ID,
              'to': recipient_number,
              'msg': message,
              'json': '1'}
    sms_ru_url = 'https://sms.ru/sms/send'
    response = requests.post(sms_ru_url, params=params)
    response.raise_for_status()
    return response.ok


def generate_or_update_verification_code(phone_number):
    code = random.randint(1000, 9999)
    sms_verification_code_instance, created = SmsVerificationCode.objects.get_or_create(
        phone_number=phone_number,
        defaults={'code': code}
    )
    if not created:
        sms_verification_code_instance.code = code
        sms_verification_code_instance.save()
    #return send_sms(phone_number, code)
    return True
