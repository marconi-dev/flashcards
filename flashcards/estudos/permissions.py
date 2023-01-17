from rest_framework.permissions import BasePermission

from baralhos.models.models import BaralhoInfoExtra

class TerminouDeRevisar(BasePermission):
    def has_permission(self, request, view):
        if request.method != 'PUT': return True
        
        baralho_pk = view.kwargs.get('baralho_pk')
        baralho = BaralhoInfoExtra.objects.get(pk=baralho_pk)

        pk = view.kwargs.get('pk')
        carta_foi_vista = baralho.cartas.get(pk=pk).vista
        nao_tem_cartas_para_revisar = not baralho.cartas_para_revisar.exists()
        
        if carta_foi_vista: return True 
        else: return nao_tem_cartas_para_revisar
        
