from datetime import date, timedelta

from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from cadastro_e_login.models import User
from baralhos.models.models import Tag, Baralho, Carta, Frente, Verso

class MesaViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('mesa-list')
        self.url_detail = reverse('mesa-detail', kwargs={'pk':40})

        self.user = User.objects.create(
            username='Username test',
            email='test@email.com',
            password='password', #Senha não criptografada
        )
    
        #SEM TAG
        self.baralhos_sem_tag = [
            Baralho.objects.create(
                usuario=self.user,
                nome=f'Baralho de teste {i}',
                publico=True,
            ) for i in range(1, 10+1)
        ]

        #IDIOMAS
        tag_idiomas = Tag.objects.create(nome='idiomas')
        self.baralhos_tag_idiomas = [
            Baralho.objects.create(
                usuario=self.user,
                nome=f'Baralho de teste {i} ({str(tag_idiomas)})',
                publico=True,
            ) for i in range(1, 10+1)
        ]
        for baralho in self.baralhos_tag_idiomas:
            baralho.tags.add(tag_idiomas)

        #ENEM
        tag_enem = Tag.objects.create(nome='ENEM')
        self.baralhos_tag_enem = [
            Baralho.objects.create(
                usuario=self.user,
                nome=f'Baralho de teste {i} ({str(tag_enem)})',
                publico=True,
            ) for i in range(1, 10+1)
        ]
        for baralho in self.baralhos_tag_enem:
            baralho.tags.add(tag_enem)

        #DUAS TAGS
        tags = [
            Tag.objects.create(nome='estudos'),
            Tag.objects.create(nome='faculdade')
        ]
        self.baralhos_com_2_tags = [
            Baralho.objects.create(
                usuario=self.user,
                nome=f'Baralho de teste {i}',
                publico=True,
            ) for i in range(1, 10+1)
        ]
        for baralho in self.baralhos_com_2_tags:
            for tag in tags:
                baralho.tags.add(tag)

    def test_get(self):
        response = self.client.get(self.url)
               
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
    
    def test_get_detail(self):
        response = self.client.get(self.url_detail)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_get_com_filtros(self):
        
        response = self.client.get(
            self.url, 
            QUERY_STRING='tags=estudos+faculdade'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_clonar_baralho(self):
        data = {}
        user2 = User.objects.create(
            username='Username2 test',
            email='test2@email.com',
            password='password', #Senha não criptografada
        )
        self.client.force_authenticate(user2)
        url_clonar = reverse('mesa-clonar-baralho', kwargs={'pk':40})
        response = self.client.post(url_clonar, data, format='json')
        
        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE
        )

    def test_mesa_list(self):
        with self.assertNumQueries(3):
            self.client.get(self.url)
    
    def test_mesa_detail(self):
        with self.assertNumQueries(3):
            self.client.get(self.url_detail)

    def test_mesa_clonar(self):
        user2 = User.objects.create(
            username='Username test2',
            email='test@email2.com',
            password='password', #Senha não criptografada
        )
        self.client.force_authenticate(user2)
        url_clonar = self.url_detail + 'clonar/'
        
        with self.assertNumQueries(1):
            self.client.post(url_clonar, format='json')
    
    def test_mesa_clonar_baralho_grande(self):
        baralho = Baralho.objects.create(
            usuario=self.user,
            nome='Meu baralho',
            publico=True
        )

        cartas = [
            Carta.objects.create(
                baralho=baralho,
                frente=Frente.objects.create(
                    texto=f'Texto da frente {i}'
                ),
                verso=Verso.objects.create(
                    texto=f'Texto do verso {i}'
                ),
                proxima_revisao=date.today(),
                criada=date.today()
            ) for i in range(100)
        ]
        user2 = User.objects.create(
            username='Username test2',
            email='test@email2.com',
            password='password', #Senha não criptografada
        )

        self.client.force_authenticate(user2)
        url_clonar = reverse('mesa-detail', kwargs={'pk':41}) + 'clonar/'
        with self.assertNumQueries(1):
            self.client.post(url_clonar, format='json')
    