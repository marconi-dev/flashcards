from datetime import date, timedelta

from django.db.models import Count, Q
from django.db import models

DIA = timedelta(days=1)
HOJE = date.today()
AMANHA = HOJE + 1*DIA

class BaralhosBaseManager(models.Manager):
    def _tags_is_valid(self, tags):
        if tags is None: return False
        if tags == '': return False
        if tags.replace(' ', '') == '': return False
        return True


    def filter_by_tags(self, tags):
        if self._tags_is_valid(tags):
            tags = tags.split(" ")
            return self.filter(tags__nome__in=tags)
        return self

class BaralhoManager(BaralhosBaseManager):
    def listar_com_info(self, tags=None):
        PARA_REVISAR = Q(cartas__vista=True) & Q(cartas__proxima_revisao=HOJE)
        
        return self.filter_by_tags(tags
            ).annotate(
            num_cartas_nao_vistas=Count('cartas', filter=Q(cartas__vista=False)
            ),num_cartas_para_revisar=Count('cartas', filter=PARA_REVISAR
            ),total_de_cartas=Count('cartas')
        ).order_by('atualizado')


    def listar_para_mesa(self, tags=None):
        return self.filter_by_tags(tags
        ).filter(publico=True
        ).only("id", "nome", "tags"
        ).prefetch_related("tags")
        
class CartaManager(BaralhosBaseManager):
    def para_revisar(self, baralho_pk):
        return self.select_related("baralho", "frente", "verso"
        ).filter(vista=True, proxima_revisao__lte=HOJE, baralho=baralho_pk
        ).order_by('criada')
    

    def __remarcar_para_amanha(self, cartas):
        """
        Remarca a proxima_revisao das cartas além do limite para amanhã
        """
        limite_diario = 20
        lista_cartas_acima_do_limite = cartas[limite_diario:]
        cartas_acima_do_limite = cartas.filter(
            id__in=[carta.id for carta in lista_cartas_acima_do_limite]
        )
        cartas_acima_do_limite.update(proxima_revisao=AMANHA)

    def para_ver(self, baralho_pk):
        cartas = self.select_related("baralho", "frente", "verso"
        ).filter(vista=False, proxima_revisao__lte=HOJE, baralho=baralho_pk
        ).order_by('criada')
        
        self.__remarcar_para_amanha(cartas)
        
        return cartas.all()