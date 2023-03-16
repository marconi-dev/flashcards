from django.db.models.signals import post_delete
from django.dispatch import receiver
from baralhos.models.models import Frente


receiver(post_delete, sender=Frente)
def apagar_imagem(instance, *args, **kwargs):
    instance.imagem.delete(save=False)
