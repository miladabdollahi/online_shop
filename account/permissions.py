from rest_framework.permissions import BasePermission
from rest_framework import exceptions
from . import utility
from .models import User


class IsExistedUser(BasePermission):
    message = {
        'data': {
            'user_is_existed': False
        }
    }

    def has_permission(self, request, view):
        phone, is_valid_phone = utility.normalize_phone(request.data.get('phone'))
        email = request.data.get('email')
        username = None
        if email:
            username = email

        if phone:
            username = phone

        if not username:
            raise exceptions.NotFound('phone and email field cant empty!')

        if not utility.is_valid_username(username):
            raise exceptions.ValidationError('email or phone is invalid!')

        if utility.is_valid_email(username) and User.objects.filter(
                email=username).exists() \
                or is_valid_phone and User.objects.filter(
            phone=username).exists():
            return True

        return False


class IsNotExistedUser(BasePermission):
    message = {
        'data': {
            'user_is_existed': True
        }
    }

    def has_permission(self, request, view):
        return not IsExistedUser().has_permission(request, view)


class IsAuthenticated(BasePermission):
    message = {
        'data': {
            'user_is_login': False
        }
    }

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
