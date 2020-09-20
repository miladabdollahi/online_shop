from rest_framework import viewsets, mixins

from product.models import Product
from product.serializers import (
    ProductSummarySerializer,
    ProductSerializer
)


class ProductSummary(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSummarySerializer


class ProductList(viewsets.GenericViewSet,
                  mixins.ListModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
