from rest_framework import serializers

from extended_lib.rest_framework.serializers import ModelSerializer
from product.models import (
    Product,
    ProductInformation,
    Color,
    Brand,
    Packaging,
    TypeOfProduct
)
from category.serializers import CategoryNestedSerializer
from specification.serializers import SpecificationSerializer


class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = ('name', 'hex_code',)


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class TypeOfProductSerializer(ModelSerializer):
    class Meta:
        model = TypeOfProduct
        fields = '__all__'


class PackagingSerializer(ModelSerializer):
    class Meta:
        model = Packaging
        fields = '__all__'


class ProductInformationSerializer(ModelSerializer):
    brand = BrandSerializer()
    type_of_product = TypeOfProductSerializer(many=True)
    packaging = PackagingSerializer()

    class Meta:
        model = ProductInformation
        fields = '__all__'


class ProductSummarySerializer(ModelSerializer):
    colors = ColorSerializer(read_only=True, many=True)
    name = serializers.ReadOnlyField(
        source='product_information.persian_name'
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'colors', 'images', 'price', 'discount',)


class ProductSerializer(ModelSerializer):
    category = CategoryNestedSerializer()
    colors = ColorSerializer(read_only=True, many=True)
    product_information = ProductInformationSerializer()
    specification = SpecificationSerializer()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ('sellers',)

    def get_tags(self, obj):
        return obj.tags.split(' ')
