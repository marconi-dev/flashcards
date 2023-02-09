from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from cadastro_e_login.models import User


class TokenViewTestCase(APITestCase):
    def setUp(self):
        #Usuario
        self.data = {
            "username":"teste",
            "email":"teste@email.com",
            "password":"senha-de-teste"}
        self.usuario = User.objects.create_user(**self.data)        

        #URLs
        self.url_renovar = reverse('renova-token')
        self.url = reverse('gera-token')

        #Request
        data = {**self.data, "username":None}
        self.response = self.client.post(self.url, data=data, format='json')

    def test_criacao_de_token(self):
        """
        gerando um token com as informações do usuário.
        """
        access_token = self.response.data.get('access')
        refresh_token = self.response.data.get('refresh')
        self.assertIsNotNone(access_token and refresh_token)
        
    def test_renovacao_de_token(self):
        """
        Renovando o access token através do refresh token
        """
        old_refresh_token = self.response.data.get('refresh')
        data = {'refresh': old_refresh_token}

        response = self.client.post(self.url_renovar, data)

        new_refresh_token = response.data.get('refresh')
        access_token = response.data.get('access')
        self.assertIsNotNone(new_refresh_token, access_token)
        self.assertNotEqual(old_refresh_token, new_refresh_token)

    def test_token_renovar_bloqueado_apos_uso(self):
        """
        Token de renovação deve ser bloqueado após uso
        """
        old_refresh_token = self.response.data.get('refresh')
        data = {'refresh': old_refresh_token}

        #Primeiro uso...
        self.client.post(self.url_renovar, data)

        #Segundo uso...
        response = self.client.post(self.url_renovar, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
