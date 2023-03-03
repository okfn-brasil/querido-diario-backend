from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..models import User


class APILoginTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

    def test_login_no_user(self):
        data = {
            "email": "email@email.com",
            "password": "password",
        }

        response = self.client.post(reverse("token_obtain_pair"), data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_user(self):
        data_login = {
            "email": "email@ok.org.br",
            "password": "password",
        }

        data_user = {
            **data_login,
            "city": "Cidade",
            "full_name": "Nome Completo",
            "gender": "m",
            "state": "UF",
            "sector": "private",
        }

        user = User.objects.create_user(**data_user)
        user.save()

        response = self.client.post(reverse("token_obtain_pair"), data_login)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
