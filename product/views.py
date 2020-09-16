from rest_framework import viewsets, mixins

from product.models import Product
from product.serializers import ProductSerializer


class ProductLists(viewsets.GenericViewSet,
                     mixins.ListModelMixin):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
