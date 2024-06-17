from abc import ABC, abstractmethod
from typing import Any, Union


class CacheInterface(ABC):
    """
    Interface para cache singleton.
    """

    @abstractmethod
    async def __aenter__(self) -> None:
        """
        Cria a instância de cache.
        """

        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Fecha a conexão com o cache.
        """

        pass

    @abstractmethod
    async def set(self, key: str, value: Any, exp: int = 86400) -> bool:
        """
        Configura o cache com expiração de 1 dia.
        """

        pass

    @abstractmethod
    async def is_cached(self, key: str) -> bool:
        """
        Verifica se a chave existe no cache.
        """

        pass

    @abstractmethod
    async def get(self, key: str) -> Union[dict, list]:
        """
        Pega o cache pela chave.
        """

        pass

    @abstractmethod
    async def clean(self) -> None:
        """
        Limpa todo o cache.
        """

        pass
