from rest_framework.response import Response
from rest_framework.views import APIView

from libs.querido_diario import QueridoDiarioABC
from libs.services import services


class SubThemesView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, **kwargs):
        querido_diario: QueridoDiarioABC = services.get(QueridoDiarioABC)
        data = querido_diario.subthemes()
        return Response(data=data, status=200)
