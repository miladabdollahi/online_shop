from django.contrib import admin

from product.models import Product, ProductInformation, Packaging, TypeOfProduct, Brand, Color

admin.site.register([Product, ProductInformation, Packaging, TypeOfProduct, Brand, Color])
