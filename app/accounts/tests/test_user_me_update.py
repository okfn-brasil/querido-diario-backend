from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..models import User


class APIUserMeUpdateTestCase(APITestCase):
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

    def test_login_put_users_me_401(self):
        response = self.client.put(reverse("users_me"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_patch_users_me_401(self):
        response = self.client.patch(reverse("users_me"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_put_users_me(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            self.data_login,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access: str = response.data.get("access", None)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)

        self.assertIsNotNone(access)
        data = {
            **self.data_user,
        }
        data["full_name"] = "Teste Name"
        data["state"] = "TO"
        data["alert_email"] = "alert_change@gmail.com"

        response = self.client.put(reverse("users_me"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("state", None), data.get("state", None))
        self.assertEqual(
            response.data.get("full_name", None), data.get("full_name", None)
        )

    def test_login_patch_users_me(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            self.data_login,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access: str = response.data.get("access", None)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)

        self.assertIsNotNone(access)
        data = {
            "full_name": "Teste Name",
        }

        response = self.client.patch(reverse("users_me"), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data.get("full_name", None), data.get("full_name", None)
        )
        self.assertEqual(
            response.data.get("state", None), self.data_user.get("state", None)
        )
