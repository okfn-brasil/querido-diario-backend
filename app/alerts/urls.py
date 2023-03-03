from rest_framework.routers import DefaultRouter

from .views import AlertViewSet

alert_router = DefaultRouter()
alert_router.register(r"", AlertViewSet, basename="alerts")


urlpatterns = [
    *alert_router.urls,
]
