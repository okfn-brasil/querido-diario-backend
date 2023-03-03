from typing import List

import requests
from rest_framework.exceptions import APIException, NotFound

from .querido_diario_abc import QueridoDiarioABC
from .serializers import GazetteFilters, GazettesResult


class QueridoDiario(QueridoDiarioABC):
    def __init__(self, api_url: str, theme) -> None:
        self.api_url: str = api_url
        self.theme: str = theme

    def cnpj_info(self, cnpj: str) -> dict:
        """get querido diario cnpj info"""

        url = f"{self.api_url}/api/company/info/{cnpj}"
        response = requests.get(url)
        if response.status_code != 200:
            raise NotFound("CNPJ não encontrado!")

        data = response.json()
        return data

    def cnpj_list_partners(self, cnpj: str) -> dict:
        """get cnpj partners list"""
        url = f"{self.api_url}/api/company/partners/{cnpj}"
        response = requests.get(url)
        if response.status_code != 200:
            raise NotFound("CNPJ não encontrado!")

        data = response.json()
        return data

    def gazettes(self, filters: GazetteFilters) -> GazettesResult:
        """get cnpj partners list"""

        url = f"{self.api_url}/api/gazettes/by_theme/{self.theme}"
        response = requests.get(url, params=filters.json())

        if response.status_code == 404:
            raise NotFound("Gazettes não encontradas!")

        data: dict = response.json()
        return GazettesResult.from_json(data)

    def entities(self) -> List[str]:
        url = f"{self.api_url}/api/gazettes/by_theme/entities/{self.theme}"
        response = requests.get(url)

        if response.status_code == 404:
            raise NotFound("Entidades não encontradas!")

        data: dict = response.json()

        entities: List[dict] = data.get("entities", None)

        if entities is None:
            raise APIException("resposta mal formatada [entities]!")

        if len(entities) != 1:
            raise APIException("resposta mal formatada [entities.length]!")

        entity_map = entities[0]

        entities_string_list = entity_map.get("entities", [])

        return entities_string_list

    def subthemes(self) -> List[str]:
        url = f"{self.api_url}/api/gazettes/by_theme/subthemes/{self.theme}"
        response = requests.get(url)

        if response.status_code == 404:
            raise NotFound("Entidades não encontradas!")

        data: dict = response.json()

        subthemes: List[str] = data.get("subthemes", None)

        if subthemes is None:
            raise APIException("resposta mal formatada [subthemes]!")

        return subthemes
