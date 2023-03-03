from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "full_name",
        "city",
        "state",
    )

    search_fields = (
        "email",
        "full_name",
    )
