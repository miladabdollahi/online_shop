from rest_framework import viewsets
from rest_framework.response import Response

from extended_lib.rest_framework import mixins
from category.models import Category
from category.serializers import CategorySerializer
from product.serializers import ProductSummarySerializer
from product.models import Product


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductFromCategoryRetrieve(viewsets.GenericViewSet,
                                  mixins.RetrieveModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        categories = []
        self.get_categories_id(instance, categories)
        products = Product.objects.filter(category_id__in=categories)
        serializer = ProductSummarySerializer(products, many=True)
        return Response({
            'error': False,
            'data': serializer.data
        })

    def get_categories_id(self, instance, categories):
        childs = instance.childs
        for child in childs.all():
            if child.childs.all().first() is None:
                categories.append(child.id)
            else:
                self.get_categories_id(child, categories)

        return categories
