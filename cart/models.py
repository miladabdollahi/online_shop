from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from product.models import Product

User = get_user_model()


class Cart(models.Model):
    STATUS_CART = (
        ('a', _('add to cart')),
        ('s', _('shipping')),
    )

    user = models.OneToOneField(to=User,
                                on_delete=models.CASCADE)

    status = models.CharField(max_length=1, verbose_name=_('status of cart'),
                              choices=STATUS_CART)

    created_datetime = models.DateTimeField(verbose_name=_('date of row creation'),
                                            auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(to=Cart,
                             on_delete=models.CASCADE, related_name='items')

    product = models.ForeignKey(to=Product,
                                on_delete=models.CASCADE, related_name='cart_items')

    color = models.CharField(max_length=150,
                             verbose_name=_('name of color'),
                             blank=True, null=True)

    size = models.CharField(max_length=150,
                            verbose_name=_('size of product'),
                            blank=True, null=True)

    number = models.SmallIntegerField(verbose_name=_('number of product'), default=1)

    created_datetime = models.DateTimeField(verbose_name=_('date of row creation'),
                                            auto_now_add=True)
