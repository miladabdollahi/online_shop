from rest_framework import routers

from . import views

app_name = 'product'
router = routers.SimpleRouter()
router.register('summary', views.ProductSummary)
router.register('', views.ProductDetail)

urlpatterns = router.urls
