from unittest import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.test import APIClient, APITestCase

from accounts.models import User
from libs.querido_diario import QueridoDiarioABC
from libs.services import services


class APICNPJTestCase(APITestCase):
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

    def login(self):
        login_response = self.client.post(
            reverse("token_obtain_pair"),
            self.data_login,
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access: str = login_response.data.get("access", None)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)

    def test_cnpj_info_get_with_user_not_found(self):
        self.login()

        self.QueridoDiarioMock.cnpj_info.side_effect = NotFound("CNPJ não encontrado!")

        response = self.client.get(
            reverse("cnpjs", kwargs={"cnpj": "12345678901234"}),
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cnpj_info_get_with_user(self):
        self.QueridoDiarioMock.cnpj_info.return_value = {
            "cnpj_completo_apenas_numeros": "12345678901234",
        }

        cnpj = "12345678901234"
        response = self.client.get(
            reverse("cnpjs", kwargs={"cnpj": cnpj}),
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data: dict = response.json()
        self.assertEqual(data.get("cnpj_completo_apenas_numeros", None), cnpj)
