from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import BaralhoViewSet, CartaViewSet


#Baralho 
baralho_router = DefaultRouter()
baralho_router.register('baralhos', BaralhoViewSet, 'baralho')
urlpatterns = baralho_router.urls

#Carta
carta_router = NestedSimpleRouter(baralho_router, 'baralhos', lookup='baralho')
carta_router.register('cartas', CartaViewSet, 'carta')
urlpatterns += carta_router.urls