from datetime import date

from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from baralhos.models.models import Tag, Baralho, Carta, Frente, Verso
from cadastro_e_login.models import User 

class CartaViewTestCase(APITestCase):
    def setUp(self):
        h = date.today()
        self.hoje = f"{h.year}-0{h.month}-{h.day}"
        
        kwargs = {
            'baralho_pk': 1,
            'pk': 1
        }
        self.url_detail = reverse('carta-detail', kwargs=kwargs)
        self.url = reverse('carta-list', kwargs={'baralho_pk': 1})
        self.user = User.objects.create(
            username='Username test',
            email='test@email.com',
            password='password', #Senha não criptografada
        )
        self.baralho = Baralho.objects.create(
            usuario=self.user,
            nome='Baralho de Teste' 
        )
        self.cartas = [
            Carta.objects.create(
                baralho=self.baralho,
                frente=Frente.objects.create(
                    texto=f'Texto da frente {i}'
                ),
                verso=Verso.objects.create(
                    texto=f'Texto do verso {i}'
                ),
                proxima_revisao=date.today()
            ) for i in range(1, 10+1)
        ]
        tag = Tag.objects.create(nome='idiomas')
        for carta in self.cartas:
            carta.tags.add(tag)

        self.client.force_authenticate(self.user)
    

    def test_carta_get(self):

        response = self.client.get(self.url)
        
        expected_data = [{
            'id': 1, 'frente': 'Texto da frente 1', 
            'verso': 'Texto do verso 1', 'nivel': 1, 
            'imagem': None, 'proxima_revisao': self.hoje, 
            'tags': ['idiomas'], 'vista': False
        }, {
            'id': 10, 'frente': 'Texto da frente 10', 
            'verso': 'Texto do verso 10', 'nivel': 1, 
            'imagem': None, 'proxima_revisao': self.hoje, 
            'tags': ['idiomas'], 'vista': False
        }]
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertListEqual(
            [
                response.data['results'][0], 
                response.data['results'][-1]
            ],
            expected_data
        )

    def test_carta_get_fail_baralho_nao_e_do_usuario(self):
        usuario_sem_baralho = User.objects.create(
            username='Username test 1',
            email='test@email1.com',
            password='password', #Senha não criptografada
        )
        self.client.force_authenticate(usuario_sem_baralho)

        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_carta_post(self):
        data = {
            'frente': 'Texto da frente da nova carta',
            'verso': 'Texto do verso da nova carta',
            'tags':"idiomas inglês poliglota"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_carta_post_fail_carta_deve_ter_um_texto_ou_uma_foto(self):
        data = {
            'verso':'Texto do verso da carta que nunca vai existir...'
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    def test_carta_detail_get(self):
        response = self.client.get(self.url_detail)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        expected_data = {
            'id':1,
            'frente': 'Texto da frente 1',
            'verso': 'Texto do verso 1',
            'nivel': 1,
            'imagem': None,
            'proxima_revisao': self.hoje,
            'tags': ['idiomas'],
            'vista': False
        }
        
        self.assertEqual(
            response.data,
            expected_data
        )
    
    def test_carta_detail_get_fail_404(self):
        url_invalida = reverse('carta-detail', kwargs={
            'baralho_pk': 1, 'pk': 9999
        })
        response = self.client.get(url_invalida)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_carta_detail_put(self):
        data = {
            'frente': 'Editado',
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_carta_detail_delete(self):
        response = self.client.delete(self.url_detail)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_carta_detail_delete_fail_404(self):
        url_invalida = reverse('carta-detail', kwargs={
            'baralho_pk': 1, 'pk': 999_999_999
        })
        response = self.client.delete(url_invalida)
        
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )


