from django.db import models
from django.utils.translation import gettext_lazy as _


class Specification(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('name of specification'),
                            blank=True, null=True)
    field_name = models.CharField(max_length=150, verbose_name=_('name of field'),
                                  blank=True, null=True)
    field_value = models.CharField(max_length=250, verbose_name=_('value of field'),
                                   blank=True, null=True)
    parent = models.ForeignKey(to='self',
                               on_delete=models.CASCADE, related_name='childs',
                               blank=True, null=True)

    class Meta:
        verbose_name = _('specification')
        verbose_name_plural = _('specifications')

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])
