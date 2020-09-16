from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Seller(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('seller')
        verbose_name_plural = _('sellers')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
