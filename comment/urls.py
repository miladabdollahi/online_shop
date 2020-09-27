from rest_framework import routers

from . import views

app_name = 'comment'
router = routers.SimpleRouter()
router.register('', views.CommentViewSet)

urlpatterns = router.urls
