from datetime import date, datetime
from rest_framework.test import APITestCase

from baralhos.models.models import Tag, Baralho, Carta, Frente, Verso
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
        tag = Tag.objects.create(nome='inglês')
        self.baralho.tags.add(tag)

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
                "criada":datetime.today()
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

    def test_filtrar_por_tags(self):
        tag_nomes  = [
            'teste', 'outra_tag', 'mais_uma','testandinho', 
            'poker', 'eletronicos','cubomagico', 'uma_tag'    
        ]
        tags = [
            Tag.objects.create(nome=nome)
            for nome in tag_nomes
        ]

        baralhos = [
            Baralho.objects.create(
                usuario=self.user, nome=f'Baralho com tag {nome}'
            ) for nome in tag_nomes
        ]

        for baralho in baralhos:
            i = baralhos.index(baralho)
            baralho.tags.add(tags[i])

        
        self.assertTrue(Baralho.objects.filter_by_tags('uma_tag').exists())
        self.assertTrue(Baralho.objects.filter_by_tags('inglês').exists())

        lista_de_tags1 = "poker teste"
        baralhos_apos_filtrar = Baralho.objects.filter_by_tags(lista_de_tags1)
        self.assertTrue(baralhos_apos_filtrar.exists())
        self.assertEqual(baralhos_apos_filtrar.count(), 2)

        lista_de_tags2 = "poker teste outra_tag mais_uma"
        baralhos_apos_filtrar = Baralho.objects.filter_by_tags(lista_de_tags2)
        self.assertTrue(baralhos_apos_filtrar.exists())
        self.assertEqual(baralhos_apos_filtrar.count(), 4)

    def test_filtrar_por_tags_typeError(self):
        with self.assertRaises(AttributeError):
            Baralho.objects.filter_by_tags(['tag_invalida'])
    


                
