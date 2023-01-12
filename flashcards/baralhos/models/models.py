from datetime import date
from django.db import models
from baralhos.models import managers


# Create your models here.
class Tag(models.Model):
    nome = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.nome


class Baralho(models.Model):
    usuario = models.ForeignKey(
        "cadastro_e_login.User", on_delete=models.CASCADE,
        related_name='baralhos'
    )
    nome = models.CharField(max_length=64)
    publico = models.BooleanField(default=False)
    atualizado = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    objects = managers.BaralhoManager()

    @property
    def total_de_cartas(self):
        return self.cartas.count()

    @property
    def cartas_nao_vistas(self):
        return self.cartas.filter(
            vista=False
        )
    
    @property 
    def num_cartas_nao_vistas(self):
        return self.cartas_nao_vistas.count()

    @property
    def cartas_para_revisar(self):
        return self.cartas.filter(
            vista=True,
            proxima_revisao=date.today()
        )

    @property
    def num_cartas_para_revisar(self):
        return self.cartas_para_revisar.count()

    def __str__(self):
        return self.nome
    

class Carta(models.Model):
    baralho = models.ForeignKey(
        Baralho, on_delete=models.CASCADE, 
        related_name='cartas'
    )
    frente = models.OneToOneField(
        'baralhos.Frente', on_delete=models.CASCADE
    )
    verso = models.OneToOneField(
        'baralhos.Verso', on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(Tag)
    proxima_revisao = models.DateField()
    vista = models.BooleanField(default=False)
    nivel = models.IntegerField(default=1)
    criada = models.DateField()
    
    objects = managers.CartaManager()


class Frente(models.Model):
    imagem = models.ImageField(
        upload_to='frente', blank=True, null=True
    )
    texto = models.CharField(
        max_length=255, null=True, blank=True
    )

    def __str__(self) -> str:
        if self.texto: return self.texto
        return f'Carta de Imagem'

class Verso(models.Model):
    texto = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.texto