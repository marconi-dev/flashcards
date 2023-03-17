#DRF
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
#DJANGO
from django.http import HttpResponseNotFound
from django.shortcuts import get_list_or_404, get_object_or_404
#FLASHCARDS
from .serializers.carta_serializers import (
    CartaSerializer, CartaCreateSerializer
)
from .serializers.baralho_serializers import (
    BaralhoDetailSerializer, BaralhoSerializer
)
from .models.models import Baralho, Carta


# Create your views here.
class BaralhoViewSet(ModelViewSet):
    serializer_class = BaralhoSerializer
    permission_classes = [IsAuthenticated]

    def apply_filtering(self, qs):
        nome = self.request.query_params.get('nome')
        usuario = self.request.user

        if nome is not None: 
            qs = qs.filter(nome__icontains=nome)

        return qs.filter(usuario=usuario)

    def get_queryset(self):
        tags = self.request.query_params.get('tags')
        queryset = Baralho.objects.listar_com_info(tags)
        queryset = self.apply_filtering(queryset)
        return queryset

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Baralho.objects.listar_com_info().get(id=pk)

    def get_serializer(self, *args, **kwargs):
        if 'many' in kwargs:
            return super().get_serializer(*args, **kwargs)

        if self.request.method == 'GET':
            baralho = self.get_object()
            return BaralhoDetailSerializer(baralho)

        if self.request.method == 'POST':
            return BaralhoSerializer(
                data=self.request.data, context={"request":self.request}
            )
        
        return super().get_serializer(*args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return HttpResponseNotFound()

    @action(['POST'], True, 'publicar', 'publicar-baralho')
    def publicar_baralho(self, request, *args, **kwargs):
        baralho = self.get_object()

        if not baralho.tags.exists():
            return Response(
                {'message':'Baralhos públicos devem possuir tags'}, 
                status.HTTP_401_UNAUTHORIZED
            )
        
        baralho.publico = True 
        baralho.save()
        return Response(
            {'message':'Baralho publicado com successo'}, 
            status.HTTP_201_CREATED
        )


class CartaViewSet(ModelViewSet):
    serializer_class = CartaSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        carta = Carta.objects.prefetch_related('tags')
        carta = carta.select_related('frente', 'verso')
        return get_object_or_404(carta, pk=pk)

    def get_queryset(self):
        kwargs = {
            'baralho__id': self.kwargs.get('baralho_pk'),
            'baralho__usuario': self.request.user
        }
        queryset = Carta.objects.filter(**kwargs)
        queryset = queryset.select_related('frente', 'verso')
        queryset = queryset.prefetch_related('baralho', 'tags')
        return get_list_or_404(queryset)
        
    def get_serializer(self, *args, **kwargs):
        """
        Modifica o serializer com base no método http, para melhor
        entendimento leia rest_framework.mixins retrieve, update, post.
        O método delete não usa nenhum serializer, e o get é o serializer
        padrão.
        """
        if self.request.method == 'POST':
            return CartaCreateSerializer(
                data=kwargs['data'], context={**self.kwargs}
            )

        if self.request.method == 'PATCH':
            return CartaCreateSerializer(
                *args, data=kwargs['data'], partial=True
            )

        return super().get_serializer(*args, **kwargs)
    
    def perform_destroy(self, instance):
        instance.frente.imagem.delete(save=False)
        return super().perform_destroy(instance)
