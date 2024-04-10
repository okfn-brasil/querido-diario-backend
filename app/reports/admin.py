from django.contrib import admin

from .models import Quotation


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "created_at",
    )

    search_fields = (
        "id",
        "email",
        "name",
    )

    list_filter = ("created_at",)
