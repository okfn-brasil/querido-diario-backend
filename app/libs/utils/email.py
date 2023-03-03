from dataclasses import dataclass
from typing import List, Optional

from django.conf import settings
from django.core.mail import send_mail


@dataclass
class Email:
    subject: str
    message: str
    email_to: List[str]
    message_html: Optional[str] = None


def send_email(email: Email):
    send_mail(
        email.subject,
        email.message,
        settings.EMAIL_HOST_USER,
        email.email_to,
        fail_silently=False,
        html_message=email.message_html,
    )
