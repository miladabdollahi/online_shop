from rest_framework import routers

from . import views

app_name = 'costumer'
router = routers.SimpleRouter()
router.register('costumers', views.CostumerViewSet)

urlpatterns = router.urls
