from django.urls import path
from rest_framework import routers

from cart import views

app_name = 'cart'

router = routers.SimpleRouter()
router.register('', views.CartItemViewSet)

urlpatterns = router.urls
