from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from account.models import User, OTP
from extended_lib.rest_framework import permissions
from account import utility
from costumer.models import Costumer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_register(request):
    phone, is_valid_phone = utility.normalize_phone(request.data.get('phone'))
    email = request.data.get('email')
    if not phone and not email:
        return Response({
            'data': {
                'msg': 'username field cant empty!'
            }
        }, status=status.HTTP_200_OK)

    if phone and not is_valid_phone:
        return Response({
            'data': {
                'msg': 'phone is invalid!'
            }
        }, status=status.HTTP_200_OK)

    if email and not utility.is_valid_email(email):
        return Response({
            'data': {
                'msg': 'email is invalid!'
            }
        }, status=status.HTTP_200_OK)

    if utility.is_valid_email(email) and User.objects.filter(
            email=email).exists() \
            or is_valid_phone and User.objects.filter(
        phone__exact=phone).exists():
        return Response({
            'data': {
                'user_is_existed': True
            }
        }, status=status.HTTP_200_OK)

    if is_valid_phone:
        otp_code = utility.get_otp_code()

        if not OTP.objects.filter(phone__exact=phone).exists():
            OTP.objects.create(phone=phone, otp_code=otp_code, otp_code_created=timezone.now())
            utility.send_message(phone, otp_code)
        elif OTP.objects.filter(phone__exact=phone, otp_is_verified=False).exists():
            otp = OTP.objects.get(phone__exact=phone)
            if not otp.is_otp_code_expired():
                return Response({
                    'data': {
                        'user_is_existed': False,
                        'otp_is_expired': False,
                        'otp_code_expired_time': otp.get_otp_code_expired_time()
                    }
                }, status=status.HTTP_200_OK)

            otp.otp_code = otp_code
            otp.otp_code_created = timezone.now()
            otp.save()
            utility.send_message(phone, otp.otp_code)

        return Response({
            'data': {
                'user_is_existed': False
            }
        }, status=status.HTTP_200_OK)

    return Response({
        'data': {
            'msg': 'you need phone number for create account!'
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsNotExistedUser])
def register_confirm(request):
    phone, is_valid_phone = utility.normalize_phone(request.data.get('phone'))
    otp_code = request.data.get('otp_code')

    if not is_valid_phone or not otp_code:
        return Response({
            'data': {
                'msg': 'phone or otp_code required!'
            }
        }, status=status.HTTP_200_OK)

    if is_valid_phone and OTP.objects.filter(phone__exact=phone, otp_is_verified=False).exists():
        otp = OTP.objects.get(phone__exact=phone)
        if not otp.is_otp_code_expired() and str(otp.otp_code) == str(otp_code):
            otp.verified_otp = True
            otp.save()
            user = User.objects.create(phone=phone)
            Costumer.objects.create(user=Costumer)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'data': {
                    'token': token.key,
                    'otp_is_verified': True,
                    'user_is_existed': True
                }
            }, status=status.HTTP_200_OK)

    return Response({
        'data': {
            'otp_is_verified': False,
            'user_is_existed': False
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsExistedUser])
def login_confirm(request):
    phone, is_valid_phone = utility.normalize_phone(request.data.get('phone'))
    email = request.data.get('email')
    password = request.data.get('password')

    if email:
        user = User.objects.get(email=email)
        token = Token.objects.get(user=user)
        return Response({
            'data': {
                'token': token.key,
                'password_is_verified': user.check_password(password)
            }
        }, status=status.HTTP_200_OK)

    if phone:
        user = User.objects.get(phone__exact=phone)
        token = Token.objects.get(user=user)
        return Response({
            'data': {
                'token': token.key,
                'password_is_verified': user.check_password(password)
            }
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsExistedUser])
def login_by_otp_confirm(request):
    phone, is_valid_phone = utility.normalize_phone(request.data.get('phone'))
    otp_code = request.data.get('otp_code')

    if not otp_code:
        return Response({
            'data': {
                'msg': 'otp code required!'
            }
        }, status=status.HTTP_200_OK)

    if is_valid_phone and OTP.objects.filter(phone__exact=phone).exists():
        otp = OTP.objects.get(phone__exact=phone)

        if not otp.is_otp_code_expired():
            if str(otp.otp_code) == str(otp_code):
                user = User.objects.get(phone=phone)
                token = Token.objects.get(user=user)
                return Response({
                    'data': {
                        'token': token.key,
                        'otp_is_verified': True
                    }
                }, status=status.HTTP_200_OK)

            return Response({
                'data': {
                    'otp_is_expired': False,
                    'otp_is_verified': False
                }
            }, status=status.HTTP_200_OK)

        return Response({
            'data': {
                'otp_is_expired': True
            }
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsExistedUser])
def send_otp_code(request):
    phone, is_valid_phone = utility.normalize_phone(request.data.get('phone'))

    if phone and OTP.objects.filter(phone__exact=phone).exists():
        otp_code = utility.get_otp_code()
        otp = OTP.objects.get(phone__exact=phone)
        if not otp.is_otp_code_expired():
            return Response({
                'data': {
                    'otp_is_expired': False,
                    'otp_code_expired_time': otp.get_otp_code_expired_time(),
                    'user_is_existed': True
                }
            }, status=status.HTTP_200_OK)

        otp.otp_code = otp_code
        otp.otp_code_created = timezone.now()
        otp.save()
        utility.send_message(phone, otp.otp_code)
        return Response({
            'data': {
                'msg': 'otp code sended',
                'otp_code_expired_time': otp.get_otp_code_expired_time(),
                'user_is_existed': True
            }
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def rest_password(request):
    password = request.data.get('password')
    phone, is_valid_phone = utility.normalize_phone(request.data.get('phone'))

    user = User.objects.get(phone__exact=phone)
    user.set_password(password)
    user.save()

    return Response({
        'data': {
            'password_is_changed': True
        }
    }, status=status.HTTP_200_OK)
