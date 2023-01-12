from rest_framework.test import APITestCase
from rest_framework import status

from django.db import connection
from django.urls import reverse

from cadastro_e_login.models import User
from baralhos.models.models import Tag, Baralho

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