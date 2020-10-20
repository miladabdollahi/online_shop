from rest_framework import permissions
from rest_framework import exceptions
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from account import utility

User = get_user_model()


class IsExistedUser(permissions.BasePermission):
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
            raise exceptions.NotFound(_('phone and email field cant empty!'))

        if not utility.is_valid_username(username):
            raise exceptions.ValidationError(_('email or phone is invalid!'))

        if utility.is_valid_email(username) and User.objects.filter(
                email=username).exists() \
                or is_valid_phone and User.objects.filter(
            phone=username).exists():
            return True

        return False


class IsNotExistedUser(permissions.BasePermission):
    message = {
        'data': {
            'user_is_existed': True
        }
    }

    def has_permission(self, request, view):
        return bool(not IsExistedUser().has_permission(request, view))


class IsAuthenticated(permissions.IsAuthenticated):
    message = {
        'data': {
            'user_is_login': False
        }
    }


class IsOwner(permissions.IsAuthenticated):
    message = {
        'data': {
            'user_is_owner': False,
            'msg': _('this user is not owner of costumer')
        }
    }

    def has_object_permission(self, request, view, obj):
        return bool(obj.user == request.user)


class IsOwnerCart(permissions.IsAuthenticated):
    message = {
        'data': {
            'costumer_is_owner': False,
            'msg': _('this user is not owner of costumer')
        }
    }

    def has_object_permission(self, request, view, obj):
        return bool(obj.cart.user == request.user)


class AllowAny(permissions.AllowAny):
    pass
