import abc


class CityABC(abc.ABC):
    @abc.abstractmethod
    def get_name(self, city_id: str) -> str:
        """get city name from ibge by city id or return city_id"""
