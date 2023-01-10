from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_list_or_404, get_object_or_404

from .serializers.carta_serializers import CartaSerializer, CartaCreateSerializer
from .serializers.baralho_serializers import BaralhoSerializer
from .models import Baralho, Carta
# Create your views here.

class BaralhoViewSet(ModelViewSet):
    serializer_class = BaralhoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Baralho.objects.filter(
            usuario=self.request.user
        )

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'POST':
            return BaralhoSerializer(
                data=self.request.data, 
                context={"request":self.request}
            )
        return super().get_serializer(*args, **kwargs)
    

class CartaViewSet(ModelViewSet):
    serializer_class = CartaSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Carta, pk=self.kwargs['pk'])

    def get_queryset(self):
        return get_list_or_404(Carta.objects.filter(
            baralho__usuario=self.request.user,
            baralho__id=self.kwargs['baralho_pk']
        ))

    def get_serializer(self, *args, **kwargs):
        """
        Modifica o serializer com base no método http, para melhor entendimento leia 
        rest_framework.mixins retrieve, update, post. O método delete não usa nenhum
        serializer, e o get é o serializer padrão.
        """
        if self.request.method == 'POST':
            return CartaCreateSerializer(
                data=kwargs['data'], context={**self.kwargs}
        )

        if self.request.method == 'PUT':
            return CartaCreateSerializer(
                *args, data=kwargs['data'], partial=True
            )
        return super().get_serializer(*args, **kwargs)
