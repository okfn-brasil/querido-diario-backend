import abc


class JSONSerializeble(abc.ABC):
    @abc.abstractmethod
    def json(self) -> dict:
        """return dict representing json"""
