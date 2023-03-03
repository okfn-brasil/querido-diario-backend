from rest_framework.response import Response
from rest_framework.views import APIView

from libs.querido_diario import QueridoDiarioABC
from libs.querido_diario.serializers import GazetteFilters, GazettesResult
from libs.services import services


class GazettesView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, **kwargs):
        self.setup_query_data()
        data = self.get_gazettes()

        return Response(data.json())

    def setup_query_data(self):
        entities = self.request.GET.getlist("entities", [])
        self.subthemes = self.request.GET.getlist("subthemes", [])
        self.territory_ids = self.request.GET.getlist("territory_ids", [])

        self.scraped_since = self.request.GET.get("scraped_since", None)
        self.scraped_until = self.request.GET.get("scraped_until", None)
        self.published_since = self.request.GET.get("published_since", None)
        self.published_until = self.request.GET.get("published_until", None)

        self.filters_data = {
            "entities": entities,
            "subthemes": self.subthemes,
            "territory_ids": self.territory_ids,
            "scraped_since": self.scraped_since,
            "scraped_until": self.scraped_until,
            "published_since": self.published_since,
            "published_until": self.published_until,
            "querystring": self.request.GET.get("querystring", None),
            "offset": self.request.GET.get("offset", None),
            "size": self.request.GET.get("size", None),
            "pre_tags": self.request.GET.get("pre_tags", None),
            "post_tags": self.request.GET.get("post_tags", None),
            "sort_by": self.request.GET.get("sort_by", None),
        }

    def get_gazettes(self) -> GazettesResult:
        querido_diario: QueridoDiarioABC = services.get(QueridoDiarioABC)
        filters = GazetteFilters(**self.filters_data)
        return querido_diario.gazettes(filters=filters)
