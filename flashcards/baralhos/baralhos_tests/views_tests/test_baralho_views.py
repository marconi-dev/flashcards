from datetime import date

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from cadastro_e_login.models import User 
from baralhos.models.models import Tag, Baralho, Carta, Frente, Verso

HOJE = date.today()
class BaralhoViewTestCase(APITestCase):
    def setUp(self):
        #URLs
        self.url_detail = reverse('baralho-detail', kwargs={'pk':1})
        self.url = reverse('baralho-list')

        #User/Auth
        self.usuario = User.objects.create(
            username='usuario',
            email='email@email.com',
            password='senha' #senha não criptografada
        ); self.client.force_authenticate(self.usuario)

        #Baralho/Tags
        self.baralho = Baralho.objects.create(
            usuario = self.usuario,
            nome='Baralho de teste',
        )
        tag = Tag.objects.create(nome='teste')
        self.baralho.tags.add(tag)

        #Cartas
        cartas = [ 
        Carta.objects.create(
            baralho=self.baralho,
            frente=Frente.objects.create(
                texto='Texto da frente'),
            verso=Verso.objects.create(
                texto='Texto do verso'),
            proxima_revisao=HOJE,
            criada=HOJE
        ) for i in range(2)]
        cartas[1].vista = True
        cartas[1].save()

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
                    'num_cartas_para_revisar': 1,
                    'total_de_cartas': 2,
                }]
            }
        )

    def _make_query_request(self, query):
        response = self.client.get(self.url, QUERY_STRING=query)
        results = response.data['results']
        return {'results': results, 'status': response.status_code}

    def test_baralhos_get_com_filtro(self):
        tags = [
            Tag.objects.create(nome='tag_generica'),
            Tag.objects.create(nome='uma_tag_bem_especifica')
        ]
        baralhos = [
            Baralho.objects.create(
                usuario=self.usuario, nome='Uma Baralho'),
            Baralho.objects.create(
                usuario=self.usuario, nome='Uma Baralho')
        ]
        [baralhos[i].tags.add(tags[i]) for i in range(2)]

        #Request com espaço vazio como tags...
        req_sem_tags=self._make_query_request('tags= ')
        self.assertEqual(req_sem_tags['status'], status.HTTP_200_OK)
        self.assertEqual(len(req_sem_tags['results']), 3)

        #Request com Tag sem nenhum baralho registrado...
        req_com_tag_vazia=self._make_query_request('tags=teste123321abc')
        self.assertEqual(req_com_tag_vazia['status'], status.HTTP_200_OK)
        self.assertEqual(len(req_com_tag_vazia['results']), 0)

        #Request com duas tags...
        req_com_2_tags=self._make_query_request('tags=tag_generica teste')
        self.assertEqual(req_com_2_tags['status'], status.HTTP_200_OK)
        self.assertEqual(len(req_com_2_tags['results']), 2)

        #Request com 3 tags
        query = 'tags=tag_generica test uma_tag_bem_especifica'
        req_com_3_tags=self._make_query_request(query)
        self.assertTrue(req_com_3_tags['status'], status.HTTP_200_OK)
        self.assertTrue(req_com_3_tags['results'], 4)

    def test_baralhos_get_com_filtro_de_nome(self):
        baralhos = [
                Baralho(nome=f'Nome de teste nº{i}', usuario=self.usuario)
                for i in range(1, 10+1)
            ]; Baralho.objects.bulk_create(baralhos)

        #Request com nome incompleto de um baralho...
        request_com_nome=self._make_query_request('nome=Nome')
        self.assertEqual(request_com_nome['status'], status.HTTP_200_OK)
        self.assertEqual(len(request_com_nome['results']), 10)
        
        #Request com nome que não deve ser encontrado...
        req_com_nome_vazio=self._make_query_request('nome=Nenhum')
        self.assertEqual(req_com_nome_vazio['status'], status.HTTP_200_OK)
        self.assertEqual(len(req_com_nome_vazio['results']), 0)

    def test_baralhos_post(self):
        data = {"nome": "Um novo Baralho",
                "tags": 'teste idiomas poliglota teste teste'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)        
        self.assertEqual(Tag.objects.count(), 3)

    def test_baralhos_post_fail_nome_nao_enviado(self):
        """
        Não é possível criar um baralho sem enviar um nome
        """
        response = self.client.post(self.url, data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_baralhos_get_detail(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_baralhos_delete(self):
        response = self.client.delete(self.url_detail)        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_publicar_baralho(self):
        response = self.client.post(self.url_detail+'publicar/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Baralho.objects.get(id=1).publico)
    
    def test_add_tags_ao_baralho(self):
        data = {'tags':"nova_tag nova_tag2 nova_tag2"} 
        response = self.client.patch(self.url_detail, data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.baralho.tags.count(), 3)
    
    def test_editar_nome_do_baralho(self):
        data = {'nome':"nome editado"} 
        response = self.client.patch(self.url_detail, data, format='json') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Baralho.objects.get(pk=1).nome, 'nome editado')
