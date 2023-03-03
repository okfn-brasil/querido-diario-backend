from unittest import mock

from rest_framework.test import APITestCase

from accounts.models import User
from libs.querido_diario import QueridoDiarioABC
from libs.services import services

from ..models import Alert
from ..tasks import DailySetupTask


class TestAlertViewSet(APITestCase):
    @classmethod
    def setUpUser(cls):
        cls.QueridoDiarioMock = mock.MagicMock(spec=QueridoDiarioABC)
        services.register(QueridoDiarioABC, cls.QueridoDiarioMock)

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

        cls.alert = Alert(
            user=cls.user,
            query_string="ffg, yj",
            territories=[
                "1501402",
            ],
            sub_themes=["tutorial", "django", "hell", "la", "SF"],
            gov_entities=["django", "hell", "SF"],
        )
        cls.alert.save()

        cls.alert_other = Alert(
            user=cls.user_other,
            query_string="ffg, yj",
            sub_themes=["tutorial", "django", "hell", "la", "SF"],
            gov_entities=["django", "hell", "SF"],
        )
        cls.alert_other.save()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.setUpUser()

    def test_daily_setup_task(self):
        alerts_ids = []

        def dummy_subtask(**kwargs):
            alert_id: str = kwargs.get("alert_id")
            alerts_ids.append(alert_id)

        task = DailySetupTask(subtask=dummy_subtask)
        task()

        alerts_ids_query = Alert.objects.values_list("id", flat=True)
        alerts_ids_query_list = [id for id in alerts_ids_query]

        self.assertEquals(alerts_ids, alerts_ids_query_list)
