from rest_framework import serializers

from cart.models import CartItem
from product.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(fields=(
        'id', 'name', 'images', 'price', 'discount', 'category', 'tags'
    ))

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'number', 'color', 'size', 'cart')
        extra_kwargs = {
            'cart': {
                'write_only': True
            }
        }


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'number', 'color', 'size', 'cart')
        extra_kwargs = {
            'cart': {
                'write_only': True
            }
        }
