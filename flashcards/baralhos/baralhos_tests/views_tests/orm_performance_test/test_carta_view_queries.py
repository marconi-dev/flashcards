from datetime import date
import random

from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from cadastro_e_login.models import User 
from baralhos.models.models import Tag, Baralho, Carta, Frente, Verso


HOJE = date.today()
class BaralhoViewListAndRetrieveTestCase(APITestCase):
    def setUp(self):
    
        self.usuario = User.objects.create(
            username='Username test',
            email='test@email.com',
            password='password', #Senha não criptografada
        )
        self.client.force_authenticate(self.usuario)

        tags = [Tag.objects.create(nome=f"tag{i}") for i in range(20)]    

        baralho = Baralho.objects.create(
            usuario=self.usuario,
            nome="Baralho de Teste",
        )
        baralho.tags.add(random.choice(tags))
            
        for i in range(100):
            Carta.objects.create(
                baralho=baralho,
                frente=Frente.objects.create(texto=f"Frente nº: {i}"),
                verso=Verso.objects.create(texto=f"Verso nº: {i}"),
                proxima_revisao=HOJE,
                criada=HOJE
            )
    
    def test_carta_list(self):
        url = reverse('carta-list', kwargs={'baralho_pk':1})
        with self.assertNumQueries(3):
            self.client.get(url)
    
    def test_carta_detail(self):
        url = reverse('carta-detail', kwargs={"baralho_pk":1, "pk":1})
        with self.assertNumQueries(2):
            self.client.get(url)