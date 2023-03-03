import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# TODO: add django-celery-beat when django 4 suport is added
# https://github.com/celery/django-celery-beat

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("querido-diario-backend")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


app.conf.beat_schedule = {
    "run-every-day-at-01am-alerts": {
        "task": "alerts.tasks.daily_setup_task",
        "schedule": crontab(hour=settings.ALERT_HOUR, minute=settings.ALERT_MINUTE),
        # 'schedule': 10.0,
    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
