from math import ceil
from datetime import date, timedelta
from django.db import models
from baralhos.models import managers


# Create your models here.
HOJE = date.today()
AMANHA = HOJE + timedelta(days=1)


class Tag(models.Model):
    nome = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.nome


class Baralho(models.Model):
    usuario = models.ForeignKey(
        "cadastro_e_login.User", 
        on_delete=models.CASCADE,
        related_name='baralhos'
    )
    nome = models.CharField(max_length=64)
    publico = models.BooleanField(default=False)
    atualizado = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    objects = managers.BaralhoManager()

    def __str__(self):
        return self.nome


class Carta(models.Model):
    baralho = models.ForeignKey(
        Baralho, 
        on_delete=models.CASCADE, 
        related_name='cartas'
    )
    frente = models.OneToOneField('baralhos.Frente', on_delete=models.CASCADE)
    verso = models.OneToOneField('baralhos.Verso', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    proxima_revisao = models.DateField()
    vista = models.BooleanField(default=False)
    nivel = models.IntegerField(default=1)
    criada = models.DateField()
    
    objects = managers.CartaManager()

    def __str__(self) -> str:
        return self.frente.texto

    def _marcar_revisao(self):
        """
        Marca a próxima revisão com base em 20% do quadrado
        do nivel da carta.
        """
        dias_ate_a_proxima_revisao = ceil(self.nivel**2 * 0.2) 
        self.proxima_revisao = HOJE + timedelta(dias_ate_a_proxima_revisao)
 
    def _reset(self):
        self.nivel = 1
        self.proxima_revisao = HOJE
        self.save()

    def estudar(self, status):
        self.vista = True
        if status == '0': return self._reset()
        elif status == '1': pass
        elif status == '2': self.nivel += 1
        elif status == '3': self.nivel += 2
        else: raise TypeError

        self._marcar_revisao()
        self.save()


class Frente(models.Model):
    imagem = models.ImageField(upload_to='frente', blank=True, null=True)
    texto = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        if self.texto: 
            return self.texto
        else: 
            return f'Carta de Imagem'


class Verso(models.Model):
    texto = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.texto