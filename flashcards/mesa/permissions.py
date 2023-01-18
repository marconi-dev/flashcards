from rest_framework import permissions
from cadastro_e_login.models import User
class UsuarioNaoDono(permissions.BasePermission):
    def has_permission(self, request, view):    
        usuario = request.user
        pk = view.kwargs['pk']

        if not usuario.baralhos.filter(id=pk).exists(): return True
        return False