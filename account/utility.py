from kavenegar import *
import random
import phonenumbers
from django.core.validators import validate_email, ValidationError
from online_shop import secure_config

api = KavenegarAPI(secure_config.Kavenegar_API_Key)


def get_otp_code():
    return random.randint(99999, 999999)


def send_message(receptor, message):
    params = {'sender': '1000596446', 'receptor': receptor,
              'message': message}
    response = api.sms_send(params)
    return response


def _is_valid_phone(phonenumber):
    try:
        phone = phonenumbers.parse(phonenumber, 'IR')
        return phonenumbers.is_valid_number(phone)
    except Exception:
        return False


def normalize_phone(phonenumber):
    try:
        phone = phonenumbers.parse(phonenumber, 'IR')
        if phonenumbers.is_valid_number(phone):
            normalized_phone = '+' + str(phone.country_code) + str(phone.national_number)
            return normalized_phone, True
        return phone, False
    except Exception:
        return None, None


def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def is_valid_username(username):
    if not _is_valid_phone(username) and not is_valid_email(username):
        return False

    return True
