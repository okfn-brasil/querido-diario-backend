import abc
from typing import List

from .serializers import GazetteFilters, GazettesResult


class QueridoDiarioABC(abc.ABC):
    @abc.abstractmethod
    def cnpj_info(self, cnpj: str) -> dict:
        """get querido diario cnpj info"""

    @abc.abstractmethod
    def cnpj_list_partners(self, cnpj: str) -> dict:
        """get cnpj partners list"""

    @abc.abstractmethod
    def gazettes(self, filters: GazetteFilters) -> GazettesResult:
        """get cnpj partners list"""

    @abc.abstractmethod
    def entities(self) -> List[str]:
        """get entities"""

    @abc.abstractmethod
    def subthemes(self) -> List[str]:
        """get subthemes"""
