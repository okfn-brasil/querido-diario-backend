from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from libs.ibge.city_abc import CityABC
from libs.querido_diario import QueridoDiarioABC
from libs.querido_diario.serializers import GazetteFilters, GazettesResult
from libs.services import services
from libs.utils.datetime import datetime_to_datetime_str_diario
from libs.utils.email import Email, send_email

from .models import Alert


class SingleAlertTask:
    def __init__(self, alert_id):
        self.alert_id = alert_id
        self.alert: Alert = Alert.objects.get(id=self.alert_id)

    def __call__(self, *args, **kwargs):
        self.get_gazettes()
        self.send_email_alert()

    def get_email(self):
        alert_email = self.alert.user.alert_email
        user_email = self.alert.user.email
        has_alert_email = alert_email is not None
        return alert_email if has_alert_email else user_email

    def get_gazettes(self):
        today = timezone.datetime.today()
        yesterday = today - timedelta(days=1)
        first_hour = timezone.datetime(
            yesterday.year, yesterday.month, yesterday.day, hour=0, minute=0, second=0
        )
        last_hour = timezone.datetime(
            today.year, today.month, today.day, hour=23, minute=59, second=59
        )
        querido_diario: QueridoDiarioABC = services.get(QueridoDiarioABC)
        self.scraped_since = datetime_to_datetime_str_diario(date=first_hour)
        self.scraped_until = datetime_to_datetime_str_diario(date=last_hour)

        self.filters = GazetteFilters(
            querystring=self.alert.query_string,
            territory_ids=self.alert.territories,
            entities=self.alert.gov_entities,
            subthemes=self.alert.sub_themes,
            scraped_since=self.scraped_since,
            scraped_until=self.scraped_until,
        )

        self.results: GazettesResult = querido_diario.gazettes(
            filters=self.filters,
        )

    def get_alert_url(self):
        base_url = settings.FRONT_BASE_URL
        url = f"{base_url}/educacao/busca?sort_by=relevance&pre_tags=<b>&post_tags=</b>"
        url += f"&scraped_since={self.scraped_since}&scraped_until={self.scraped_until}"

        if self.alert.query_string:
            url += f"&querystring={self.alert.query_string}"

        if self.alert.territories is not None and len(self.alert.territories) > 0:
            url += "&local=" + "&local=".join(self.alert.territories)

        if self.alert.sub_themes is not None and len(self.alert.sub_themes) > 0:
            url += "&subthemes=" + "&subthemes=".join(self.alert.sub_themes)

        if self.alert.gov_entities is not None and len(self.alert.gov_entities) > 0:
            url += "&entities=" + "&entities=".join(self.alert.gov_entities)

        return url

    def get_territories_names(self):
        city_api: CityABC = services.get(CityABC)
        if self.alert.territories is None:
            return []
        else:
            return [city_api.get_name(city_id) for city_id in self.alert.territories]

    def email_get_alert(self) -> Email:
        context = {
            "title": settings.PROJECT_TITLE,
            "total_gazettes": self.results.total_gazettes,
            "query_string": self.alert.query_string,
            "territory_ids": self.get_territories_names(),
            "gov_entities": self.alert.gov_entities,
            "sub_themes": self.alert.sub_themes,
            "scraped_since": self.scraped_since,
            "scraped_until": self.scraped_until,
            "url": self.get_alert_url(),
        }
        subject = f"[{settings.PROJECT_TITLE}] Encontramos novidades com seus alertas!"
        html_message = render_to_string("alerts/email.html", context)
        plain_message = strip_tags(html_message)

        return Email(
            subject=subject,
            message=plain_message,
            message_html=html_message,
            email_to=[
                self.get_email(),
            ],
        )

    def send_email_alert(self) -> None:
        if self.results.total_gazettes > 0:
            email = self.email_get_alert()
            send_email(email=email)


@shared_task
def single_alert_task(alert_id: str):
    task = SingleAlertTask(alert_id=alert_id)
    task()


class DailySetupTask:
    def __init__(self, subtask) -> None:
        self.subtask = subtask

    def __call__(self) -> None:
        alerts_ids = Alert.objects.values_list("id", flat=True)
        for alert_id in alerts_ids:
            self.subtask(alert_id=alert_id)


@shared_task
def daily_setup_task():
    task = DailySetupTask(subtask=single_alert_task.delay)
    task()
