from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from rest_framework import views, viewsets
from rest_framework.response import Response

from extended_lib.rest_framework import mixins
from extended_lib.rest_framework import permissions as perm
from cart.models import Cart, CartItem
from product.models import Product
from cart.serializers import CartItemSerializer, CartItemCreateSerializer


class AddToCart(views.APIView):
    permission_classes = (perm.IsAuthenticated,)

    def post(self, request, format=None):
        cart_item = request.data.get('cart_item')
        if Cart.objects.filter(costumer__user=request.user).exists():
            if not CartItem.objects.filter(
                    product=cart_item.get('id'),
                    cart__costumer=request.user.costumer).exists():

                data = {
                    'cart': request.user.costumer.cart.pk,
                    'product': cart_item.get('id'),
                    'color': cart_item.get('color'),
                    'size': cart_item.get('size'),
                    'number': cart_item.get('number', 1)
                }
                serializer = CartItemCreateSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({
                    'error': False,
                    'data': serializer.data
                })
            else:
                return Response({
                    'error': True,
                    'data': {
                        'msg': _('this product existed in cart')
                    }
                })
        else:
            return Response({
                'error': True,
                'data': {
                    'msg': _('don\'t existed cart for this user')
                }
            })


class CartItemViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (perm.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(cart=request.user.costumer.cart))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        sum_price = Product.objects.filter(
            cart_items__in=queryset
        ).aggregate(Sum('price'))
        return Response({
            'error': False,
            'data': {
                'items': serializer.data,
                'total_price': sum_price.get('price__sum')
            }
        })
