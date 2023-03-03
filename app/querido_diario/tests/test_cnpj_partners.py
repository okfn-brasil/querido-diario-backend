from unittest import mock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from accounts.models import User
from libs.querido_diario import QueridoDiarioABC
from libs.services import services


class APICNPJPartnersTestCase(APITestCase):
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

    def test_cnpj_partners_get_without_user(self):
        self.QueridoDiarioMock.cnpj_list_partners.return_value = []
        response = self.client.get(
            reverse("cnpjs_partners", kwargs={"cnpj": "12345678901234"}),
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_cnpj_partners_get_with_user_not_found(self):
        self.login()
        self.QueridoDiarioMock.cnpj_list_partners.return_value = []
        response = self.client.get(
            reverse("cnpjs_partners", kwargs={"cnpj": "60691894000135"}),
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data: list = response.json()
        self.assertEquals(len(data), 0)

    def test_cnpj_partners_get_with_user(self):
        self.login()
        cnpj = "12345678901234"
        self.QueridoDiarioMock.cnpj_list_partners.return_value = [
            {"cnpj_completo_apenas_numeros": cnpj},
        ]
        response = self.client.get(
            reverse("cnpjs_partners", kwargs={"cnpj": cnpj}),
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data: list = response.json()
        self.assertEqual(len(data), 1)
