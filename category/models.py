from django.db import models
from django.utils.translation import gettext_lazy as _

from specification.models import Specification


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('name of category'))
    parent = models.ForeignKey(to='self',
                               on_delete=models.CASCADE, related_name='childs',
                               default=None)
    specification = models.ForeignKey(to=Specification,
                                      on_delete=models.DO_NOTHING, related_name='categories',
                                      default=None)
