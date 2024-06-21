from typing import TypeVar, Generic
from abc import ABCMeta, abstractmethod

MODEL = TypeVar("MODEL")


class RequestRepositoryInterface(Generic[MODEL], metaclass=ABCMeta):
    """
    Interface para gerar o repositório de consulta a APIs
    """

    @abstractmethod
    async def list(self, limit: int, offset: int) -> list[MODEL]:
        """
        Método responsável por listar dados de uma API.
        """

        pass

    @abstractmethod
    async def find_by_id(self, id: int) -> MODEL:
        """
        Método responsável por encontrar um determinado objeto na API.
        """

        pass
