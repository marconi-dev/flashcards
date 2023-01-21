from datetime import date
import random

from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from django.db.models import Count, F, Q

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

        for i in range(100):
            baralho = Baralho.objects.create(
                usuario=self.usuario,
                nome=f"Baralho de Teste nº: {i}",
            )
            baralho.tags.add(random.choice(tags))
            
            Carta.objects.create(
                baralho=baralho,
                frente=Frente.objects.create(texto=f"Frente nº: {i}"),
                verso=Verso.objects.create(texto=f"Verso nº: {i}"),
                proxima_revisao=HOJE,
                criada=HOJE
            )
    
    def test_110_baralhos_e_110_cartas(self):
        self.assertEqual(Baralho.objects.count(), 100)
        self.assertEqual(Carta.objects.count(), 100)

    def test_baralho_list_view(self):
        url = reverse('baralho-list')
        with self.assertNumQueries(2):
            self.client.get(url)
    
    