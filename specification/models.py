from django.db import models
from django.utils.translation import gettext_lazy as _


class Specification(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('name of specification'))
    field_name = models.CharField(max_length=150, verbose_name=_('name of field'))
    field_value = models.CharField(max_length=250, verbose_name=_('value of field'))
    parent = models.ForeignKey(to='self',
                               on_delete=models.CASCADE, related_name='childs',
                               default=None)
