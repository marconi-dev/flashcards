from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from cadastro_e_login.models import User


class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('criar-usuario')

    def test_usuario_criado_com_sucesso(self):
        data = {
            "username":"teste",
            "email":"teste@email.com",
            "password":"senha-de-teste"}
        response = self.client.post(self.url, data)
        usuario = User.objects.filter(username='teste')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(usuario.exists())
        
    def test_usuario_nao_foi_criado_informacoes_invalidas(self):
        data = {"compo_invalido":"teste"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
