from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from extended_lib.rest_framework import mixins
from category.models import Category
from category.serializers import CategorySerializer
from product.serializers import ProductSummarySerializer
from product.models import Product


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(parent=None))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'error': False,
            'data': serializer.data
        })

    @action(detail=True, url_path='products', url_name='products_of_category')
    def products(self, request, *args, **kwargs):
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
        if childs.all().first():
            for child in childs.all():
                if child.childs.all().first() is None:
                    categories.append(child.id)
                else:
                    self.get_categories_id(child, categories)
        else:
            categories.append(instance.id)
        return categories
