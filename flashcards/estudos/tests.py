from datetime import date, timedelta

from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from cadastro_e_login.models import User
from baralhos.models.models import Tag, Baralho, BaralhoInfoExtra, Carta, Frente, Verso
# Create your tests here.

class EstudosTestCase(APITestCase):
    def setUp(self):
        #setup urls
        kwargs = {'baralho_pk': 1,}
        self.url = reverse('estudos-list', kwargs=kwargs)
        
        #setup usuario
        self.user = User.objects.create(
            username='Username test',email='test@email.com',
            password='password', #Senha não criptografada
        )
        self.client.force_authenticate(self.user)
        
        #setup baralho
        baralho_info = {
            'nome': 'Baralho de Teste', 
            'usuario': self.user
        }
        self.baralho = BaralhoInfoExtra.objects.create(**baralho_info)
        self.tag = Tag.objects.create(nome='teste')
        self.baralho.tags.add(self.tag)
        
        #setup cartas

        self.cartas_nao_vistas = self.__set_cartas(
            vista=False, prox_revisao=date.today(),
            txt='Uma carta para ver'
            )
        
        tres_dias_atras = date.today() - timedelta(days=3)
        self.cartas_vistas = self.__set_cartas(
            vista=True, prox_revisao=tres_dias_atras,
            txt='Uma carta para revisar'
        )

    def __set_cartas(self, vista, prox_revisao,txt):
        txt
        return [
            Carta.objects.create(
                baralho=self.baralho,
                frente=Frente.objects.create(texto=txt),
                verso=Verso.objects.create(texto=txt),
                criada=prox_revisao,
                proxima_revisao=prox_revisao,
                vista=vista
            ) for i in range(1, 40+1)
        ]

    def test_get_successo(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_cartas_para_revisar_tem_prioridade(self):
        """
        A view deve retornar cartas não vistas somento após o usuário não ter nenhuma carta para revisar
        """
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code, 
            status.HTTP_200_OK
        )

        #O teste a seguir se baseia no fato de que a view retorna no máximo 20
        #cartas não vista.
        num_cartas_retornadas = len(response.data['results'])
        self.assertTrue(num_cartas_retornadas > 20)

    def test_apos_estudar_libera_as_cartas_nao_vistas(self):
        for carta in self.cartas_vistas: carta.estudar('3')
        
        response = self.client.get(self.url)
        self.assertEqual(len(response.data['results']), 20)
        self.assertGreater(self.baralho.cartas_nao_vistas.count(), 20)
        
    def test_ver_nova_carta_antes_de_revisar(self):

        data = {"status": '3'}

        url = reverse('estudos-detail', kwargs={'baralho_pk':1, 'pk':1})
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
    
    def test_estudar_carta(self):
        data = {"status": "1"}
        url = reverse('estudos-detail', kwargs={'baralho_pk':1, 'pk':41})
        
        response = self.client.put(url, data, format='json')
        self.assertEqual(
            response.status_code, 
            status.HTTP_200_OK
        )
    
    