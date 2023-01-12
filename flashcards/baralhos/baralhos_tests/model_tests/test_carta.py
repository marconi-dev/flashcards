from datetime import datetime

from rest_framework.test import APITestCase

from cadastro_e_login.models import User
from baralhos.models.models import (
    Baralho, Carta, Frente, Verso
)


class CartaTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='Usuario de Teste',
            email="email@email.com",
            password="pass" # senha não criptografada
        )
        data = {
            "usuario":self.user,
            "nome":"Baralho de Teste"
        }
        self.baralho = Baralho.objects.create(**data)

        self.frente = Frente.objects.create(
            texto='Esta é a frente'
        )
        self.verso = Verso.objects.create( 
            texto='Este é o verso'
        )
        self.carta = Carta.objects.create(
            baralho=self.baralho, 
            frente=self.frente, verso=self.verso,
            proxima_revisao=datetime.today(),
            criada=datetime.today()
        )

    
    def test_carta_criada_com_sucesso(self):
        
        self.assertTrue(
            Carta.objects.filter(
                baralho__nome='Baralho de Teste'
            )
        )
        self.assertEqual(
            self.frente, self.carta.frente
        )
        self.assertEqual(
            self.verso, self.carta.verso
        )
        self.assertFalse(
            self.carta.vista
        )

    def teste_ORM_configurada_corretamente(self):
        """
        Testa a configuração dos "related_names" 
        """
        self.assertEqual(
            self.baralho.cartas.first(),
            self.carta
        )  
        
        self.assertEqual(
            self.frente.carta,
            self.carta
        )

        self.assertEqual(
            self.verso.carta,
            self.carta
        )
