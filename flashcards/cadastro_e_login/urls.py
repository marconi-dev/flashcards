from .views import UserView
from django.urls import path 
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

urlpatterns = [ 
    path('token/', TokenObtainPairView.as_view(), name='gera-token'),
    path('renovar/', TokenRefreshView.as_view(), name='renova-token'),
]


urlpatterns += [
    path('criar-usuario/', UserView.as_view(), name='criar-usuario')
]

