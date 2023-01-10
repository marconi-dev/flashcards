from datetime import date
from rest_framework.test import APITestCase

from baralhos.models import Baralho, Carta, Frente, Verso
from cadastro_e_login.models import User

class BaralhoTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="Usuario de Teste",
            email="email@email.com",
            password="pass" #senha não criptografada
        )
        data = {
            "usuario":self.user,
            "nome":"Baralho de Teste",
        }
        self.baralho = Baralho.objects.create(**data)

        infos = [
            {
                "baralho":self.baralho,
                "proxima_revisao": date.today(),
                "frente": Frente.objects.create(
                    texto=f"Texto da frente"
                ),
                "verso": Verso.objects.create(
                    texto=f"Texto do verso"
                ),
            } for i in range(1, 10+1)
        ]
        for info in infos:
            Carta.objects.create(**info)



    def test_baralho_criado_com_sucesso(self):
        """
        Testa a criação correto de um Baralho
        """
        self.assertTrue(
            Baralho.objects.filter(nome='Baralho de Teste').exists()
        )
        self.assertEqual(
            str(self.baralho),
            "Baralho de Teste"
        )

    def test_ORM_configurada_corretamente(self):
        """
        Testa os "related_names" 
        """
        self.assertEqual(
            self.user.baralhos.first(),
            self.baralho
        )

    def test_cartas_filtradas_corretamente(self):
        """
        Testa se as "properties" estão funcionando como o esperado
        """
        for i in range(5, 10+1):
            carta = Carta.objects.get(id=i)
            carta.vista = True; carta.save()
    
        self.assertListEqual(
            list(self.baralho.cartas_nao_vistas.values('id')),
            [{'id': i} for i in range(1, 4+1)]
        )

        self.assertEqual(
            self.baralho.num_cartas_nao_vistas, 4
        )

        self.assertListEqual(
            list(self.baralho.cartas_para_revisar.values('id')),
            [{'id': i} for i in range(5, 10+1)]
        )

        self.assertEqual(
            self.baralho.num_cartas_para_revisar, 6
        )
       