from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from extended_lib.rest_framework import mixins
from extended_lib.rest_framework import permissions as perm
from cart.models import Cart, CartItem
from product.models import Product
from cart.serializers import CartItemSerializer, CartItemCreateSerializer


class CartItemViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin):
    queryset = CartItem.objects.all()
    permission_classes = (perm.IsOwnerCart,)

    def get_serializer_class(self):
        if self.action == 'list':
            return CartItemSerializer
        elif self.action == 'add_to_cart':
            return CartItemCreateSerializer

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

    @action(methods=['post'], detail=False, url_path='add-to-cart', url_name='add-to-cart')
    def add_to_cart(self, request, *args, **kwargs):
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
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response({
                    'error': False,
                    'data': serializer.data,
                }, status=status.HTTP_201_CREATED, headers=headers)
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