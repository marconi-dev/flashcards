from datetime import date, timedelta
from rest_framework.test import APITestCase

from cadastro_e_login.models import User
from baralhos.models.models import (
    Baralho, Carta, Frente, Verso
)

HOJE = date.today()
DIA = timedelta(days=1)
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
            proxima_revisao=HOJE,
            criada=HOJE
        )

    
    def test_carta_criada_com_sucesso(self):
        
        self.assertTrue(
            Carta.objects.filter(baralho__nome='Baralho de Teste')
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
            self.baralho.cartas.first(), self.carta
        )  
        self.assertEqual(
            self.frente.carta, self.carta
        )
        self.assertEqual(
            self.verso.carta, self.carta
        )

    def test_metodo_estudar_define_vista_como_true(self):
        self.carta.estudar('0')
        self.assertTrue(self.carta.vista)

    def test_metodo_estudar_com_status_0(self):
        self.carta.estudar('0')
        self.assertEqual(self.carta.proxima_revisao, HOJE)
    
    def test_metodo_estudar_com_status_1(self):
        self.carta.estudar('1')
        self.assertEqual(self.carta.proxima_revisao, HOJE + (1*DIA))

    def test_metodo_estudar_com_status_1_e_nivel_7(self):
        self.carta.nivel = 7; self.carta.estudar('1')
        self.assertEqual(self.carta.proxima_revisao, HOJE + (10*DIA))

    def test_metodo_estudar_com_status_2(self):
        self.carta.estudar('2')
        self.assertEqual(self.carta.proxima_revisao, HOJE + (1*DIA))
    
    def test_metodo_estudar_com_status_2_e_nivel_7(self):
        self.carta.nivel = 7; self.carta.estudar('2')
        self.assertEqual(self.carta.proxima_revisao, HOJE + (13*DIA))

    def test_metodo_estudar_com_status_3(self):
        self.carta.estudar('3')
        self.assertEqual(self.carta.proxima_revisao, HOJE + (2*DIA))

    def test_metodo_estudar_com_status_3_e_nivel_7(self):
        self.carta.nivel = 7; self.carta.estudar('3')
        self.assertEqual(self.carta.proxima_revisao, HOJE + (17*DIA))

    def test_metodo_estudar_status_invalido(self):
            with self.assertRaises(TypeError):
                self.carta.estudar('-42')
                self.carta.estudar('teste')

