from django.contrib import admin

from cart.models import Cart, CartItem

admin.site.register([Cart, CartItem])
