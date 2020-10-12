from django.urls import path
from rest_framework import routers

from cart import views

app_name = 'cart'

router = routers.SimpleRouter()
router.register('', views.CartItemViewSet)

urlpatterns = router.urls + [
    path('add-to-cart', views.AddToCart.as_view(), name='add-to-cart'),
]
