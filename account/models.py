from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from account import utility


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone:
            raise ValueError('The given phone must be set')
        phone, is_valid_phone = utility.normalize_phone(phone)
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    username = None
    USERNAME_FIELD = 'phone'

    email = models.EmailField()
    phone = models.CharField(max_length=128,
                             unique=True)
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return str(self.phone)


class OTP(models.Model):
    phone = models.CharField(max_length=128,
                             unique=True)
    otp_code = models.SmallIntegerField()
    otp_code_created = models.DateTimeField(verbose_name=_('otp code created date'))
    otp_code_expire_time = models.FloatField(default=180,
                                             verbose_name=_('otp code expire time'))
    is_active = models.BooleanField(default=False)
    otp_is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name=_('otp table row created date'))

    class Meta:
        verbose_name = _('otp')
        verbose_name_plural = _('otps')

    def get_otp_code_expired_time(self):
        return self.otp_code_expire_time - (timezone.now().timestamp() - self.otp_code_created.timestamp())

    def is_otp_code_expired(self):
        diff_time = timezone.now().timestamp() - self.otp_code_created.timestamp()
        if diff_time > self.otp_code_expire_time:
            return True

        return False
