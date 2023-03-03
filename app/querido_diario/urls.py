from django.urls import path

from .views import (
    CNPJPartnersView,
    CNPJSView,
    EntitiesView,
    GazettesView,
    SubThemesView,
)

urlpatterns = [
    path("cnpjs/<str:cnpj>/", CNPJSView.as_view(), name="cnpjs"),
    path(
        "cnpjs/<str:cnpj>/partners", CNPJPartnersView.as_view(), name="cnpjs_partners"
    ),
    path("gazettes/", GazettesView.as_view(), name="gazettes"),
    path("entities/", EntitiesView.as_view(), name="entities"),
    path("subthemes/", SubThemesView.as_view(), name="subthemes"),
]
