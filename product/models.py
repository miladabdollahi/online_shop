from django.db import models
from django.utils.translation import gettext_lazy as _

from seller.models import Seller
from specification.models import Specification
from category.models import Category
from online_shop import settings


class Color(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('name of color'))
    hex_code = models.CharField(max_length=250, verbose_name=_('code of color'))

    class Meta:
        verbose_name = _('color')
        verbose_name_plural = _('colors')

    def __str__(self):
        return self.name


class Brand(models.Model):
    TYPE_OF_BRAND_CHOICES = (
        ('IR', _('iranian brand')),
        ('EN', _('foreign brand'))
    )
    english_name = models.CharField(max_length=250, verbose_name=_('english name of brand'))
    persian_name = models.CharField(max_length=250, verbose_name=_('persian name of brand'))
    image = models.ImageField(verbose_name=_('image of brand'), upload_to='images')
    type = models.CharField(verbose_name=_('type of brand'), max_length=2,
                            choices=TYPE_OF_BRAND_CHOICES, default='IR')
    brand_description = models.TextField()
    logo = models.ImageField(verbose_name=_('logo of brand'), help_text=_('height and width 600 X 600 px'),
                             width_field=600, height_field=600, upload_to='images')
    judiciary_brand_registration_form = models.ImageField(upload_to='images')
    judiciary_site_link = models.URLField()

    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')

    def __str__(self):
        if settings.LANGUAGE_CODE == 'fa-IR':
            return self.persian_name
        else:
            return self.english_name


class TypeOfProduct(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('name of type'))
    value = models.CharField(max_length=250, verbose_name=_('value of type'))

    class Meta:
        verbose_name = _('product type')
        verbose_name_plural = _('product types')

    def __str__(self):
        return self.value


class Packaging(models.Model):
    width = models.PositiveIntegerField(verbose_name=_('width'))
    height = models.PositiveIntegerField(verbose_name=_('height'))
    length = models.PositiveIntegerField(verbose_name=_('length'))
    weight = models.PositiveIntegerField(verbose_name=_('weight'))

    class Meta:
        verbose_name = _('packing')
        verbose_name_plural = _('packaging')


class ProductInformation(models.Model):
    english_name = models.CharField(max_length=250, verbose_name=_('english name of product'))
    persian_name = models.CharField(max_length=250, verbose_name=_('persian name of product'))
    is_fake = models.BooleanField(verbose_name=_('originality of product'))
    brand = models.ForeignKey(to=Brand,
                              on_delete=models.DO_NOTHING, related_name='product_informations',
                              verbose_name=_('brand'), blank=True, null=True)
    type_of_product = models.ManyToManyField(to=TypeOfProduct,
                                             verbose_name=_('type'))
    packaging = models.ForeignKey(to=Packaging,
                                  on_delete=models.DO_NOTHING, related_name='product_informations',
                                  verbose_name=_('packaging'))
    description_of_product = models.TextField(verbose_name=_('description of product'),
                                              blank=True, null=True)
    positive_points = models.CharField(max_length=250, verbose_name=_('positive points'),
                                       blank=True, null=True)
    negative_points = models.CharField(max_length=250, verbose_name=_('negative points'),
                                       blank=True, null=True)

    class Meta:
        verbose_name = _('product information')
        verbose_name_plural = _('product informations')

    def __str__(self):
        if settings.LANGUAGE_CODE == 'fa-IR':
            return self.persian_name
        else:
            return self.english_name


class Product(models.Model):
    sellers = models.ManyToManyField(to=Seller,
                                     related_name='products', verbose_name=_('sellers'))
    category = models.ForeignKey(to=Category,
                                 on_delete=models.DO_NOTHING, related_name='products',
                                 verbose_name=_('category'))
    colors = models.ManyToManyField(to=Color,
                                    verbose_name=_('colors'))
    product_information = models.ForeignKey(to=ProductInformation,
                                            on_delete=models.DO_NOTHING, related_name='products',
                                            verbose_name=_('information of product'))
    specification = models.ForeignKey(to=Specification,
                                      on_delete=models.DO_NOTHING, related_name='products',
                                      verbose_name=_('specification'))
    tags = models.CharField(max_length=150, verbose_name=_('tag of product'))
    images = models.ImageField(verbose_name=_('images of product'), upload_to='images')
    price = models.CharField(max_length=50, verbose_name=_('price of product'))
    discount = models.CharField(max_length=3, verbose_name=_('discount'),
                                blank=True, null=True)
    guarantee = models.CharField(max_length=150, verbose_name=_('name of guarantee'),
                                 blank=True, null=True)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return str(self.product_information)
