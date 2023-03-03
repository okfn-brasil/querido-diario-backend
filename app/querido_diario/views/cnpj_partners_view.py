from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from libs.querido_diario import QueridoDiarioABC
from libs.services import services


class CNPJPartnersView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, **kwargs):
        cnpj = kwargs.get("cnpj", None)
        if cnpj is None:
            raise ValidationError({"cnpj": "cnpj deve ser informado"})

        querido_diario: QueridoDiarioABC = services.get(QueridoDiarioABC)
        data = querido_diario.cnpj_list_partners(cnpj=cnpj)
        return Response(data)
