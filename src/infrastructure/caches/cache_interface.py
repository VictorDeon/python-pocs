from abc import ABC, abstractmethod
from typing import Any, Union


class CacheInterface(ABC):
    """
    Interface para cache singleton.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.cache = None

    @abstractmethod
    async def __aenter__(self) -> None:
        """
        Cria a instância de cache.
        """

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Fecha a conexão com o cache.
        """

    @abstractmethod
    async def set(self, key: str, value: Any, exp: int = 86400) -> bool:
        """
        Configura o cache com expiração de 1 dia.
        """

    @abstractmethod
    async def is_cached(self, key: str) -> bool:
        """
        Verifica se a chave existe no cache.
        """

    @abstractmethod
    async def get(self, key: str) -> Union[dict, list]:
        """
        Pega o cache pela chave.
        """

    @abstractmethod
    async def clean(self) -> None:
        """
        Limpa todo o cache.
        """
