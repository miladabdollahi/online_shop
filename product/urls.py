from . import views
from rest_framework import routers

app_name = 'product'
router = routers.SimpleRouter()
router.register('', views.ProductLists)

urlpatterns = router.urls
