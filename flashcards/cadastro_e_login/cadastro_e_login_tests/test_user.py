from rest_framework.test import APITestCase
from ..models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.data = {
            "username":"teste",
            "email":"teste@email.com",
            "password":"senha-de-teste"
        }
        self.user = User.objects.create_user(**self.data)


    def test_usuario_criado_com_successo(self):
        """
        Usuário pode ser criado com um email, um username e uma senha
        """
        self.assertTrue(
            User.objects.filter(email=self.data['email']).exists()
        )       
    

    def test_senha_esta_criptografada(self):
        """
        A senha criada para o usuario está criptografada.
        Testando pois o usuario padrão foi substituido.
        """
        self.assertNotEqual(
            self.user.password,
            self.data['password']
        )