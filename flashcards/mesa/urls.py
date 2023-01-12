from rest_framework.routers import DefaultRouter
from mesa.views import MesaViewSet


router = DefaultRouter()
router.register('mesa', MesaViewSet, 'mesa')

urlpatterns = router.urls
