from rest_framework.permissions import BasePermission

from baralhos.models.models import Carta


class TerminouDeRevisar(BasePermission):
    """
    O usuário só pode ver uma NOVA carta depois de terminar 
    a revisão das cartas que já foram vistas.
    """
    def has_permission(self, request, view):
        if request.method != 'PUT': return True
        
        baralho_pk = view.kwargs.get('baralho_pk')
        pk = view.kwargs.get('pk')

        carta_nao_vista = not Carta.objects.values("vista").get(pk=pk)['vista']
        cartas_para_revisar = Carta.objects.para_revisar(baralho_pk).exists()

        if carta_nao_vista and cartas_para_revisar: 
            return False
        return True
