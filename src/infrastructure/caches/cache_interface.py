from abc import ABC, abstractmethod
from typing import Any, Union


class CacheSingletonInterface(ABC):
    """
    Interface para cache singleton.
    """

    __instance = None

    def __init__(self):
        """
        Construtor.
        """

        if self.__instance is not None:
            raise RuntimeError("A instância de cache já existe. Utilize o método get_instance().")

    @classmethod
    def get_instance(cls):
        """
        Pega a instância do cache.
        """

        if cls.__instance is None:
            cls.__instance = cls()
            cls.__instance.create_instance()

        return cls.__instance

    @abstractmethod
    def create_instance(self) -> None:
        """
        Cria a instância de cache.
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

    @abstractmethod
    async def close(self) -> None:
        """
        Fecha a conexão com o cache.
        """

        pass
