from django.urls import path

from .views import QuotationCreateApiView

urlpatterns = [
    path("quotation/", QuotationCreateApiView.as_view(), name="quotation"),
]
