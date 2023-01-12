from rest_framework.viewsets import GenericViewSet

from flashcards.baralhos.models.models import Baralho
# Create your views here.

class MesaViewSet(GenericViewSet):
    queryset = Baralho.objects.filter(
        publico=True
    ).values_list('id', 'nome', 'tags')