from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from extended_lib.rest_framework import mixins
from product.models import Product
from product.serializers import (
    ProductSummarySerializer,
    ProductSerializer
)
from comment.models import Comment
from comment.serializers import CommentsOfProductSerializer


class ProductSummary(viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSummarySerializer


class ProductDetail(viewsets.GenericViewSet,
                    mixins.RetrieveModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(methods=['GET'], detail=True, url_path='comments', url_name='comments_of_product')
    def comments(self, request, *args, **kwargs):
        instance = self.get_object()
        comments = Comment.objects.filter(product=instance.pk)
        serializer = CommentsOfProductSerializer(comments, many=True)
        return Response({
            'error': False,
            'data': serializer.data
        })