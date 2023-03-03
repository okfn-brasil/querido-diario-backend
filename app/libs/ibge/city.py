import ssl

import requests
import urllib3

from .city_abc import CityABC


class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context,
        )


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount("https://", CustomHttpAdapter(ctx))
    return session


class City(CityABC):
    def get_name(self, city_id: str) -> str:
        api = (
            f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{city_id}"
        )

        try:
            response = get_legacy_session().get(api)
        except Exception:
            return city_id

        if response.status_code != 200:
            return city_id

        try:
            data = response.json()
            return data["nome"]
        except Exception:
            return city_id
