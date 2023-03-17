from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from django.urls import path
from .views import user_apiview


urlpatterns = [ 
    # simple_jwt
    path('conta/token/', TokenObtainPairView.as_view(), name='gera-token'),
    path('conta/renovar/', TokenRefreshView.as_view(), name='renova-token'),
    # flashcards
    path('conta/', user_apiview, name='criar-usuario')
]
