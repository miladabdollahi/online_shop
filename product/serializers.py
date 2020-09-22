from rest_framework import serializers

from product.models import (
    Product,
    ProductInformation,
    Color
)
from category.serializers import CategoryNestedSerializer


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('name', 'hex_code',)


class ProductInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInformation


class ProductSummarySerializer(serializers.ModelSerializer):
    colors = ColorSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('id', 'colors', 'images', 'price', 'discount')


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryNestedSerializer()
    colors = ColorSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        exclude = 'seller'
