from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User


class Costumer(models.Model):
    national_code = models.CharField(verbose_name=_('national code'),
                                     blank=True, null=True,
                                     max_length=50
                                     )
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    birth_day = models.DateField(verbose_name=_('date of birth'),
                                 blank=True, null=True
                                 )

    job = models.CharField(verbose_name=_('job'),
                           blank=True, null=True,
                           max_length=150
                           )
    bank_card = models.IntegerField(verbose_name=_('bank card number'),
                                    blank=True, null=True
                                    )
