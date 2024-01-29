import random

import requests

from BeautyCity.settings import SMS_RU_API_ID
from users.models import CustomUser


def send_sms(recipient_number, message):
    params = {'api_id': SMS_RU_API_ID,
              'to': recipient_number,
              'msg': message,
              'json': '1'}
    sms_ru_url = 'https://sms.ru/sms/send'
    response = requests.post(sms_ru_url, params=params)
    response.raise_for_status()
    sms_response = response.json()
    if sms_response['sms_response'] == 'OK':
        return response.ok
    else:
        return False


def generate_or_update_verification_code(phone_number):
    code = random.randint(1000, 9999)
    sms_verification_code_instance, created = CustomUser.objects.get_or_create(
        phone_number=phone_number,
        defaults={'code': code}
    )
    if not created:
        sms_verification_code_instance.code = code
        sms_verification_code_instance.save()
    return send_sms(phone_number, code)
