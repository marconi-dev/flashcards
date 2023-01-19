from datetime import date

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet as GViewSet
from rest_framework import status
from rest_framework.mixins import (
    ListModelMixin as LMixin, RetrieveModelMixin as RMixin
)

from django.core.cache import cache

from mesa.permissions import UsuarioNaoDono
from baralhos.models.models import Baralho, Carta, Frente, Verso
from mesa.serializers import (
    SimpleBaralhoSerializer, DetailBaralhoSerializer
)
# Create your views here.

HOJE = date.today()

class MesaViewSet(LMixin, RMixin, GViewSet):
    serializer_class = DetailBaralhoSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        return Baralho.objects.listar_com_info().get(id=pk)

    def get_cached_queryset(self):
        queryset = cache.get('mesa_list_queryset')
        if queryset is None:
            queryset = Baralho.objects.listar_para_mesa()
            cache.set('mesa_list_queryset', queryset, 5 * 60)

        return queryset

    def get_queryset(self):
        tags = self.request.query_params.get('tags')

        if tags is not None: 
            return Baralho.objects.listar_para_mesa(tags)

        return self.get_cached_queryset()



    def get_serializer(self, *args, **kwargs):
        if 'many' in kwargs: return SimpleBaralhoSerializer(*args, many=True)

        return super().get_serializer(*args, **kwargs)



    def __clonar_frente_e_verso(self, carta):
        return {
            'nova_frente': Frente.objects.create(
                imagem=carta.frente.imagem,
                texto=carta.frente.texto
        ),
            'novo_verso': Verso.objects.create(
                texto=carta.verso.texto
        )
        }
        
    def __clonar_cartas(self, novo_baralho):
        baralho = self.get_object()
        novas_cartas = list()

        for carta in baralho.cartas.iterator():
            info = self.__clonar_frente_e_verso(carta)

            nova_carta = Carta.objects.create(
                proxima_revisao=HOJE,
                baralho=novo_baralho,
                criada=carta.criada,
                frente=info['nova_frente'],
                verso=info['novo_verso'],
            )
            novas_cartas.append(nova_carta)

        for antiga_carta in baralho.cartas.iterator():
            for tag in antiga_carta.tags.iterator():
                for carta in novas_cartas:
                    carta.tags.add(tag)

    @action(['POST'], url_name='clonar-baralho', url_path='clonar',
        permission_classes=[IsAuthenticated, UsuarioNaoDono], detail=True)
    def clonar_baralho(self, request, *args, **kwargs):
        baralho = self.get_object()
        novo_baralho = Baralho.objects.create(
            usuario=self.request.user,
            nome=baralho.nome
        )
        for tag in baralho.tags.iterator():
            novo_baralho.tags.add(tag)

        self.__clonar_cartas(novo_baralho)
        return Response(
            {'message':'baralho clonado com successo'},
            status.HTTP_201_CREATED
        )