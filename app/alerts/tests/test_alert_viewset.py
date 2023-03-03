from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from accounts.models import User

from ..models import Alert


class TestAlertViewSet(APITestCase):
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

        cls.user_other = User.objects.create_user(
            email="email1@ok.org.br",
            password="password",
            city="Cidade",
            full_name="Nome Completo1",
            gender="m",
            state="UF",
            sector="private",
        )
        cls.user_other.save()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.setUpUser()
        cls.client = APIClient()

    def login(self):
        login_response = self.client.post(
            reverse("token_obtain_pair"),
            self.data_login,
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access: str = login_response.data.get("access", None)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)

    def setup_alert(self):
        self.alert = Alert(
            user=self.user,
            query_string="ffg, yj",
            territories=[
                "1501402",
            ],
            sub_themes=["tutorial", "django", "hell", "la", "SF"],
            gov_entities=["django", "hell", "SF"],
        )
        self.alert.save()
        self.alert_other = Alert(
            user=self.user_other,
            query_string="ffg, yj",
            territories=[
                "1501402",
            ],
            sub_themes=["tutorial", "django", "hell", "la", "SF"],
            gov_entities=["django", "hell", "SF"],
        )
        self.alert_other.save()

    def test_list_empty(self):
        self.login()
        response = self.client.get(reverse("alerts-list"))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEquals(data.get("results", None), [])

    def test_list_with_one(self):
        self.login()
        self.setup_alert()
        response = self.client.get(reverse("alerts-list"))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEquals(data.get("count", None), 1)
        results = data.get("results", None)
        self.assertNotEquals(results, None)
        self.assertEquals(len(results), 1)
        alert = results[0]
        self.assertEquals(alert["id"], str(self.alert.id))

    def test_create_one(self):
        self.login()
        alert_data = {
            "user": str(self.user.id),
            "query_string": "query, string",
            "territory_id": "1501402",
            "sub_themes": ["SFA", "DSEI"],
            "gov_entities": [
                "SESAI",
            ],
        }
        user_alerts = Alert.objects.filter(user=self.user)
        self.assertEquals(len(user_alerts), 0)
        response = self.client.post(reverse("alerts-list"), data=alert_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        user_alerts = Alert.objects.filter(user=self.user)
        self.assertEquals(len(user_alerts), 1)

    def test_patch_user_alert(self):
        self.login()
        self.setup_alert()

        user_alerts = Alert.objects.filter(user=self.user)
        self.assertEquals(len(user_alerts), 1)

        alert_data = {
            "query_string": "new query",
            "territories": [
                "1501403",
            ],
            "sub_themes": ["SFA", "DSEI"],
            "gov_entities": [
                "SESAI",
                "FUNASA",
                "FUNAI",
            ],
        }
        response = self.client.patch(
            reverse("alerts-detail", kwargs={"pk": str(self.alert.id)}),
            data=alert_data,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        alert: Alert = Alert.objects.get(pk=self.alert.pk)
        self.assertEquals(alert.query_string, alert_data["query_string"])
        self.assertListEqual(alert.territories, alert_data["territories"])
        self.assertEquals(alert.sub_themes, alert_data["sub_themes"])
        self.assertEquals(alert.gov_entities, alert_data["gov_entities"])

    def test_delete_user_alert(self):
        self.login()
        self.setup_alert()

        user_alerts = Alert.objects.filter(user=self.user)
        self.assertEquals(len(user_alerts), 1)
        response = self.client.delete(
            reverse("alerts-detail", kwargs={"pk": str(self.alert.id)})
        )
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        user_alerts = Alert.objects.filter(user=self.user)
        self.assertEquals(len(user_alerts), 0)

    def test_delete_another_user_alert(self):
        self.login()
        self.setup_alert()

        user_alerts = Alert.objects.filter(user=self.user)
        self.assertEquals(len(user_alerts), 1)
        response = self.client.delete(
            reverse("alerts-detail", kwargs={"pk": str(self.alert_other.id)})
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        user_alerts = Alert.objects.filter(user=self.user)
        self.assertEquals(len(user_alerts), 1)
