from django.conf import settings
from django.db import transaction
from reports.models import Quotation
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView

from libs.utils.email import Email, send_email

from ..serializers import QuotationSerializer


class QuotationCreateApiView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = QuotationSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            quotation: Quotation = serializer.save()
            message = f"{quotation.id}\n"
            message += f"{quotation.name}\n"
            message += f"{quotation.email}\n"
            message += f"{quotation.message}\n"

            try:
                subject = f"Cotação de relatório de {quotation.name}"
                send_email(
                    email=Email(
                        subject=subject,
                        email_to=[settings.QUOTATION_TO_EMAIL],
                        message=message,
                    )
                )
            except Exception as e:
                raise APIException(f"Erro ao mandar email: {e}")
            return quotation
