from rest_framework import viewsets

from extended_lib.rest_framework import mixins
from product.models import Product
from product.serializers import (
    ProductSummarySerializer,
    ProductSerializer
)


class ProductSummary(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSummarySerializer


class ProductDetail(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
