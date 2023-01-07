from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from ..models import User



class TokenViewTestCase(APITestCase):
    def setUp(self):
        self.data = {
            "username":"teste",
            "email":"teste@email.com",
            "password":"senha-de-teste"
        }
        self.usuario = User.objects.create_user(**self.data)        

        self.url_renovar = reverse('renova-token')
        self.url = reverse('gera-token')

        data = {**self.data, "username":None}
        self.response = self.client.post(self.url, data=data, format='json')

    def test_criacao_de_token(self):
        """
        gerando um token com as informações do usuário.
        """
       
        
        self.assertIsNotNone(
            self.response.data['access'] and self.response.data['refresh']
        )
    
    def test_renovacao_de_token(self):
        """
        Renovando o access token através do refresh token
        """
        token_renovar = {
            'refresh': self.response.data['refresh']
        }
        response = self.client.post(self.url_renovar, token_renovar)
        

        self.assertIsNotNone(
            response.data['access'] and response.data['refresh']
        )
        self.assertNotEqual(
            self.response.data['refresh'],
            response.data['refresh']
        )

    def test_token_renovar_bloqueado_apos_uso(self):
        """
        Token de renovação deve ser bloqueado após uso
        """
        token_renovar = {
            'refresh': self.response.data['refresh']
        }

        #Primeiro uso
        self.client.post(self.url_renovar, token_renovar)
        
        response = self.client.post(self.url_renovar, token_renovar)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )        
        

        
        