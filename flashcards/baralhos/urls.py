from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import BaralhoViewSet, CartaViewSet

router = DefaultRouter()
router.register('baralhos', BaralhoViewSet, 'baralho')
urlpatterns = router.urls

carta_router = NestedSimpleRouter(router, 'baralhos', lookup='baralho')
carta_router.register('cartas', CartaViewSet, 'carta')
urlpatterns += carta_router.urls