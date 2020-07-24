from django.contrib.auth.backends import ModelBackend
from phonenumber_field.phonenumber import to_python
from account.models import User


class EmailPhoneBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if username is None or password is None:
            return
        phone = to_python(username)
        if phone and phone.is_valid():
            try:
                user = User.objects.get(phone=phone)
            except User.DoesNotExist:
                User().set_password(password)
            else:
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
        else:
            return super(EmailPhoneBackend, self).authenticate(request, username=username, password=password, **kwargs)
