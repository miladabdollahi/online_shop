from rest_framework import routers

from . import views

app_name = 'category'
router = routers.SimpleRouter()
router.register('', views.CategoryViewSet)

urlpatterns = router.urls
