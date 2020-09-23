from rest_framework import serializers

from product.models import (
    Product,
    Color
)
from category.serializers import CategoryNestedSerializer


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('name', 'hex_code',)


class ProductSummarySerializer(serializers.ModelSerializer):
    colors = ColorSerializer(read_only=True, many=True)
    name = serializers.ReadOnlyField(
        source='product_information.persian_name'
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'colors', 'images', 'price', 'discount')


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryNestedSerializer()
    colors = ColorSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        exclude = 'seller'
