from rest_framework import routers

from . import views

app_name = 'product'
router = routers.SimpleRouter()
router.register('summary', views.ProductSummary)

urlpatterns = router.urls
