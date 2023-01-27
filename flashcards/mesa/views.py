from datetime import date

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet as GViewSet
from rest_framework import status
from rest_framework.mixins import (
    ListModelMixin as LMixin, RetrieveModelMixin as RMixin
)

from django.db import connection
from django.core.cache import cache

from mesa.permissions import UsuarioNaoDono
from baralhos.models.models import Tag, Baralho, Carta, Frente, Verso
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



    def __clonar_frente_e_verso(self, cartas):
        ultimas_index = cartas.count()
        versos, frentes = list(), list()

        for carta in cartas.iterator():
            frentes.append(Frente(
                texto=carta.frente.texto
            ))
            versos.append(Verso(
                texto=carta.verso.texto
            ))

        Frente.objects.bulk_create(frentes)
        Verso.objects.bulk_create(versos)

        frentes = Frente.objects.only('id').order_by('id'
        ).reverse()[:ultimas_index]
        versos = Verso.objects.only('id').order_by('id'
        ).reverse()[:ultimas_index]
        
        return {'frentes': frentes, 'versos': versos}

    def __clonar_cartas(self, novo_baralho):
        baralho = self.get_object()
        cartas = Carta.objects.select_related('baralho', 'frente', 'verso').filter(baralho=baralho).order_by('criada')
        id_dict = self.__clonar_frente_e_verso(cartas)

        novas_cartas = list()

        for i, carta in enumerate(reversed(cartas)):

            novas_cartas.append(Carta(
                proxima_revisao=HOJE,
                baralho=novo_baralho,
                criada=carta.criada,
                frente=id_dict['frentes'][i],
                verso=id_dict['versos'][i],
            ))
        Carta.objects.bulk_create(novas_cartas)      
        
    def __gerar_novo_baralho(self, baralho):
        novo_baralho = Baralho.objects.create(
            usuario=self.request.user,
            nome=baralho.nome
        )
        return novo_baralho
    
    def __clonar_tags(self, tags, model):
        model.tags.add(*tags)

    @action(
        methods=['POST'], 
        url_name='clonar-baralho', 
        url_path='clonar',
        permission_classes=[
            IsAuthenticated, UsuarioNaoDono
        ], 
        detail=True
    )
    def clonar_baralho(self, request, *args, **kwargs):
        return Response(
            {'message': 'Este serviço está em manutenção'}, 
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
        baralho = self.get_object()
        tags = Tag.objects.filter(baralho=baralho)
        novo_baralho = self.__gerar_novo_baralho(baralho)

        self.__clonar_tags(tags, novo_baralho)
        self.__clonar_cartas(novo_baralho)
        return Response(
            {'message':'baralho clonado com successo'},
            status.HTTP_201_CREATED
        )