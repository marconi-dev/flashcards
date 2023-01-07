from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from ..models import User

class UserViewSetTestCase(APITestCase):
    

    def test_usuario_criado_com_sucesso(self):
        url = reverse('criar-usuario')

        data = {
            "username":"teste",
            "email":"teste@email.com",
            "password":"senha-de-teste"
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertTrue(
            User.objects.filter(username='teste').exists()
        )
        
    def test_usuario_nao_foi_criado_informacoes_invalidas(self):
        url = reverse('criar-usuario')
        data = {
            "compo_invalido":"teste"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )