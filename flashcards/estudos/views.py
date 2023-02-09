from datetime import date

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import (GenericViewSet as GViewSet)
from rest_framework.mixins import ( 
    ListModelMixin as LMixin, 
    RetrieveModelMixin as RMixin,
    UpdateModelMixin as UMixin
)

from django.shortcuts import get_object_or_404

from estudos.permissions import TerminouDeRevisar
from estudos.serializers import EstudosSerializer
from baralhos.models.models import Carta


# Create your views here.
HOJE = date.today()
class EstudosViewSet(LMixin, RMixin, UMixin, GViewSet):
    serializer_class = EstudosSerializer
    permission_classes = [IsAuthenticated, TerminouDeRevisar]
    
    def get_queryset(self):
        """
        Retorna as cartas com revisão para hoje ou as 20 
        primeiras cartas não vistas. 
        """
        baralho_pk = self.kwargs.get('baralho_pk')
        cartas_para_revisar = Carta.objects.para_revisar(baralho_pk)        
        cartas_para_ver = Carta.objects.para_ver(baralho_pk)

        if cartas_para_revisar.exists(): return cartas_para_revisar
        
        return cartas_para_ver

    def update(self, request, *args, **kwargs):
        """
        Performa a ação de estudar uma carta.
        """
        pk = self.kwargs.get('pk')
        status_da_carta = request.data.get('status')
        
        carta_filter = Carta.objects.filter(proxima_revisao__lte=HOJE)
        carta = get_object_or_404(carta_filter, pk=pk)
        
        if status_da_carta is None:        
            return Response(
                {"message":"Não foi informado um status de estudo"}, 
                status.HTTP_400_BAD_REQUEST)
        
        carta.estudar(status_da_carta)
        return Response({'message':'ok'}, status.HTTP_200_OK)
