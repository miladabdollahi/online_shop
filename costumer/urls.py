from django.urls import path
from . import views
from rest_framework import routers

app_name = 'costumer'
router = routers.SimpleRouter()
router.register('costumers', views.CostumerViewSet)

urlpatterns = router.urls
