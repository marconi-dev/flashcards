from rest_framework.routers import DefaultRouter

mesa_router = DefaultRouter()
mesa_router.register('mesa', MesaViewSet, 'mesa')
