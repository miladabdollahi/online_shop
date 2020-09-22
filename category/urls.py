from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register('', views.CategoryViewSet)
router.register('products', views.ProductFromCategoryRetrieve)

urlpatterns = router.urls
