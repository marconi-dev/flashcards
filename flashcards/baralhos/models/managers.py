from datetime import date, timedelta

from django.db.models import Count, Q
from django.db import models

DIA = timedelta(days=1)
HOJE = date.today()
AMANHA = HOJE + 1*DIA

class BaralhosBaseManager(models.Manager):
    def filter_by_tags(self, tags): 
        return self.filter(tags__nome__in=tags)
        

class BaralhoManager(BaralhosBaseManager):
    def listar_com_info(self):
        para_revisar = Q(cartas__vista=True) & Q(cartas__proxima_revisao=HOJE)
        return self.annotate(
            num_cartas_nao_vistas=Count('cartas', filter=Q(cartas__vista=False)
            ),num_cartas_para_revisar=Count('cartas', filter=para_revisar
            ),total_de_cartas=Count('cartas')
        ).order_by('atualizado')

    def listar_para_mesa(self, tags=None):
        baralhos = self.filter(publico=True
        ).only("id", "nome", "tags"
        ).prefetch_related("tags")

        if tags: baralhos = baralhos.filter(tags__nome__in=tags)
        
        return baralhos

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
        list_cartas_acima_do_limite = cartas[limite_diario:]
        cartas_acima_do_limite = cartas.exclude(
            id__in=[carta.id for carta in list_cartas_acima_do_limite]
        )
        cartas_acima_do_limite.update(proxima_revisao=AMANHA)


    def para_ver(self, baralho_pk):
        cartas = self.select_related("baralho", "frente", "verso"
        ).filter(vista=False, proxima_revisao__lte=HOJE, baralho=baralho_pk
        ).order_by('criada')
        
        self.__remarcar_para_amanha(cartas)
        
        return cartas.all()