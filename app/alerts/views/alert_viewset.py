from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Alert
from ..serializers import AlertSerializer


class AlertViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AlertSerializer

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
