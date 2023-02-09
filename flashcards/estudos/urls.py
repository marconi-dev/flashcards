from rest_framework_nested.routers import NestedSimpleRouter as NSRouter

from baralhos.urls import baralho_router
from estudos.views import EstudosViewSet


estudos_router = NSRouter(baralho_router, 'baralhos', lookup='baralho')
estudos_router.register('estudos', EstudosViewSet, 'estudos')

urlpatterns = estudos_router.urls
