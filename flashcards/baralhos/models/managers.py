from datetime import date

from django.db.models import Count, Q
from django.db import models

HOJE = date.today()
class BaralhosBaseManager(models.Manager):
    def filter_by_tags(self, tags):
        queryset = self.all()
        for tag in tags:
            queryset = queryset.filter(
                tags__nome__contains=tag.lower()
            )
        return queryset

class BaralhoManager(BaralhosBaseManager):
    def listar_com_info(self):
        para_revisar = Q(cartas__vista=True) & Q(cartas__proxima_revisao=HOJE)

        return self.annotate(
            num_cartas_nao_vistas=Count(
                'cartas', filter=Q(cartas__vista=False)
            ),
            num_cartas_para_revisar=Count(
                'cartas', filter=para_revisar
            ),
            total_de_cartas=Count('cartas')
        )

class CartaManager(BaralhosBaseManager):
    pass
