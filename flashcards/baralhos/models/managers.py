from django.db import models

class BaralhosBaseManager(models.Manager):
    def filter_by_tags(self, tags):
        queryset = self.all()
        for tag in tags:
            queryset = queryset.filter(
                tags__nome__contains=tag.lower()
            )
        return queryset

class BaralhoManager(BaralhosBaseManager):
    pass

class CartaManager(BaralhosBaseManager):
    pass
