from rest_framework import serializers

from .models import Quotation


class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = (
            "id",
            "name",
            "email",
            "message",
            "created_at",
        )

        read_only_fields = (
            "id",
            "created_at",
        )
