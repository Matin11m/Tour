import json
from kavenegar import *
from django.conf import settings


def send_otp(phone, verification_code):
    if not settings.DEBUG:
        try:
            api = KavenegarAPI(settings.KAVEHNEGAR_API_KEY)
            params = {
                'sender': settings.KAVEHNEGAR_SENDER,
                'receptor': phone,
                'message': f'کد فعال سازی شما {verification_code} است. به هیچ عنوان در اختیار دیگران قرار ندهید!'
            }   
            response = api.sms_send(params)
            return response
        except APIException as e:
            return str(e)
        except HTTPException as e: 
            return str(e)