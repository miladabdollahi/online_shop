from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from product.models import Product

User = get_user_model()


class Comment(models.Model):
    STATUS_CHOICES = (
        ('a', _('accepted')),
        ('w', _('awaiting approval')),
        ('n', _('not approved'))
    )
    user = models.ForeignKey(to=User,
                             on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(to=Product,
                                on_delete=models.CASCADE, related_name='comments')
    title = models.CharField(max_length=250, verbose_name=_('title of comment'),
                             blank=True)
    positive_points = models.CharField(max_length=250, verbose_name=_('positive points'),
                                       blank=True)
    negative_points = models.CharField(max_length=250, verbose_name=_('negative points'),
                                       blank=True)
    text = models.TextField(verbose_name=_('text of comment'))
    status = models.CharField(max_length=1, verbose_name=_('status of comment'),
                              choices=STATUS_CHOICES, default='w'
                              )
    created_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        if self.title:
            return self.title

        return self.product.product_information.persian_name
