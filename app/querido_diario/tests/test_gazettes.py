from unittest import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from accounts.models import User
from libs.querido_diario import QueridoDiarioABC
from libs.querido_diario.serializers import GazettesResult
from libs.services import services


class APIGazettesTestCase(APITestCase):
    @classmethod
    def setUpUser(cls):
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
        cls.user = User.objects.create_user(**cls.data_user)

        cls.user.save()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.setUpUser()
        cls.QueridoDiarioMock = mock.MagicMock(spec=QueridoDiarioABC)
        services.register(QueridoDiarioABC, cls.QueridoDiarioMock)
        cls.QueridoDiarioMock.gazettes.return_value = GazettesResult(
            total_gazettes=0,
            gazettes=[],
        )

    def login(self):
        login_response = self.client.post(
            reverse("token_obtain_pair"),
            self.data_login,
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access: str = login_response.data.get("access", None)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)

    def test_gazettes_get_without_user(self):
        response = self.client.get(
            reverse("gazettes"),
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_gazettes_get_with_user(self):
        self.login()
        response = self.client.get(
            reverse("gazettes"),
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
