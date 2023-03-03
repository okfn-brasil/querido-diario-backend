from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..models import User


class APIUserMeGetTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

        cls.data_login = {
            "email": "email@ok.org.br",
            "password": "password",
        }

        cls.data_user = {
            **cls.data_login,
            "city": "Cidade",
            "full_name": "Nome Completo",
            "gender": "m",
            "state": "UF",
            "sector": "private",
        }
        user = User.objects.create_user(**cls.data_user)
        user.save()

    def test_login_get_users_me_no_acces_token(self):
        response = self.client.get(reverse("users_me"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_get_users_me(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            self.data_login,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access: str = response.data.get("access", None)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)

        self.assertIsNotNone(access)

        response = self.client.get(reverse("users_me"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
