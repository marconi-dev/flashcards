from rest_framework.viewsets import GenericViewSet as GViewSet
from rest_framework.mixins import (
    ListModelMixin as LMixin, RetrieveModelMixin as RMixin
)

from baralhos.models.models import Baralho
from mesa.serializers import (
    SimpleBaralhoSerializer, DetailBaralhoSerializer
)
# Create your views here.

class MesaViewSet(LMixin, RMixin, GViewSet):
    serializer_class = DetailBaralhoSerializer

    def get_queryset(self):
        tags = self.request.query_params.get('tags')

        if tags is not None:
            queryset = Baralho.objects.filter_by_tags(tags.split(' '))
            queryset = queryset.filter(publico=True)
            return queryset 

        return Baralho.objects.filter(publico=True)

    def get_serializer(self, *args, **kwargs):
        
        if 'many' in kwargs:
            return SimpleBaralhoSerializer(*args, many=True)

        return super().get_serializer(*args, **kwargs)

    