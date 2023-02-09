from rest_framework.test import APITestCase
from cadastro_e_login.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.data = {
            "username":"teste",
            "email":"teste@email.com",
            "password":"senha-de-teste"}
        self.user = User.objects.create_user(**self.data)

    def test_usuario_criado_com_successo(self):
        """
        Usuário pode ser criado com um email, um username e uma senha
        """
        email = self.data['email']
        self.assertTrue(User.objects.filter(email=email).exists())       

    def test_senha_esta_criptografada(self):
        """
        A senha criada para o usuario está criptografada.
        """
        senha_em_texto = self.data['password']
        senha_criptografada = self.user.password
        self.assertNotEqual(senha_em_texto, senha_criptografada)
