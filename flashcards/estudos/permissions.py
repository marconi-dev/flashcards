from rest_framework.permissions import BasePermission

from baralhos.models.models import Carta

class TerminouDeRevisar(BasePermission):
    def has_permission(self, request, view):
        if request.method != 'PUT': return True
        
        baralho_pk = view.kwargs.get('baralho_pk')
        pk = view.kwargs.get('pk')

        carta_foi_vista = Carta.objects.values("vista").get(pk=pk)['vista']
        cartas_para_revisar = Carta.objects.para_revisar(baralho_pk).exists()

        if carta_foi_vista: return True
        if cartas_para_revisar: return False
        else: return True
        
