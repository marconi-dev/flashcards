from datetime import date

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from cadastro_e_login.models import User 
from baralhos.models.models import Tag, Baralho, Carta, Frente, Verso

class BaralhoViewTestCase(APITestCase):
    def setUp(self):
        self.url_detail = reverse('baralho-detail', kwargs={'pk':1})
        self.url = reverse('baralho-list')

        self.usuario = User.objects.create(
            username='usuario',
            email='email@email.com',
            password='senha' #senha não criptografada
        )
        self.client.force_authenticate(self.usuario)
        
        self.baralho = Baralho.objects.create(
            usuario = self.usuario,
            nome='Baralho de teste',
        )
        tag = Tag.objects.create(nome='teste')
        self.baralho.tags.add(tag)

        info = [{
            "baralho":self.baralho,
            "frente": Frente.objects.create(
                texto="Texto da frente"
            ),
            "verso": Verso.objects.create(
                texto="Texto do verso"
            ),
            "proxima_revisao": date.today()
        } for i in range(2)]
        Carta.objects.create(**info[0])
        Carta.objects.create(**info[1], vista=True)

    def test_baralhos_get(self):
        response = self.client.get(self.url, format='json')

        self.assertEqual(
            response.data,
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [{
                    'id': 1,
                    'nome': 'Baralho de teste',
                    'num_cartas_nao_vistas': 1,
                    'num_cartas_para_revisar': 1
                }]
            }
        )

    def test_baralhos_post(self):
        data = {
            "nome": "Um novo Baralho",
            "tags": 'teste idiomas poliglota teste teste'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        
        self.assertEqual(Tag.objects.count(), 3)

    def test_baralhos_post_fail_nome_nao_enviado(self):
        """
        Não é possível criar um baralho sem enviar um nome
        """
        response = self.client.post(self.url, data={}, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    def test_baralhos_get_detail(self):
        response = self.client.get(self.url_detail)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_baralhos_delete(self):
            response = self.client.delete(self.url_detail)
            
            self.assertEqual(
                response.status_code,
                status.HTTP_204_NO_CONTENT
            )
