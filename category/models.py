from django.db import models
from django.utils.translation import gettext_lazy as _

from specification.models import Specification


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('name of category'))
    parent = models.ForeignKey(to='self',
                               on_delete=models.CASCADE, related_name='childs',
                               blank=True, null=True)
    specification = models.ForeignKey(to=Specification,
                                      on_delete=models.DO_NOTHING, related_name='categories',
                                      blank=True, null=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['parent__id']

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])
