from rest_framework import serializers

from extended_lib.rest_framework.serializers import ModelSerializer
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


class ProductSummarySerializer(ModelSerializer):
    colors = ColorSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('colors', 'images', 'price', 'discount', 'id')


class ProductSerializer(ModelSerializer):
    category = CategoryNestedSerializer()
    colors = ColorSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        exclude = 'seller'
