import json
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
            "proxima_revisao": date.today(),
            "criada":date.today()
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

    def _make_query_request(self, query):
        response = self.client.get(self.url, QUERY_STRING='tags='+query)
        response.render()
        json_body = json.loads(response.content)
        results = json_body['results']

        return {'results': results, 'status': response.status_code}

    def test_baralhos_get_com_filtro(self):
        tags = [
            Tag.objects.create(nome='tag_generica'),
            Tag.objects.create(nome='uma_tag_bem_especifica')
        ]
        baralho = Baralho.objects.create(
            usuario=self.usuario, nome='Uma baralho')
        baralho2 = Baralho.objects.create(
            usuario=self.usuario, nome='Uma baralho')
        
        baralho.tags.add(tags[0])
        baralho2.tags.add(tags[1])


        req_sem_tags=self._make_query_request(' ')
        self.assertEqual(req_sem_tags['status'], status.HTTP_200_OK)
        self.assertEqual(len(req_sem_tags['results']), 3)

        req_com_tag_vazia=self._make_query_request('teste123321abc')
        self.assertEqual(req_com_tag_vazia['status'], status.HTTP_200_OK)
        self.assertEqual(len(req_com_tag_vazia['results']), 0)

        req_com_2_tags=self._make_query_request('tag_generica teste')
        self.assertEqual(req_com_2_tags['status'], status.HTTP_200_OK)
        self.assertEqual(len(req_com_2_tags['results']), 2)

        req_com_3_tags=self._make_query_request(
            'tag_generica test uma_tag_bem_especifica')
        self.assertTrue(req_com_3_tags['status'], status.HTTP_200_OK)
        self.assertTrue(req_com_3_tags['results'], 4)

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
            status.HTTP_404_NOT_FOUND
        )

    def test_baralhos_delete(self):
            response = self.client.delete(self.url_detail)
            
            self.assertEqual(
                response.status_code,
                status.HTTP_204_NO_CONTENT
            )

    def test_publicar_baralho(self):
        response = self.client.post(self.url_detail+'publicar/')

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertTrue(
            Baralho.objects.get(id=1).publico
        )
    
    def test_add_tags_ao_baralho(self):
        data = {
            'tags':"nova_tag nova_tag2 nova_tag2"
        }
        
        response = self.client.patch(self.url_detail, data, format='json')
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(self.baralho.tags.count(), 3)
    
    def test_editar_nome_do_baralho(self):
        data = {
            'nome':"novo nome do baralho"
        }
        
        response = self.client.patch(self.url_detail, data, format='json')
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        baralho = Baralho.objects.get(pk=1)
        self.assertEqual(
            baralho.nome, 'novo nome do baralho'
        )