from abc import abstractmethod
from typing import Any, List


class StorageSingletonInterface:
    """
    Faz a instrumentalização do storage usando o singleton.
    """

    __instance = None

    def __init__(self) -> None:
        """
        Construtor do cliente.
        """

        if self.__instance is not None:
            raise RuntimeError("A instância do storage já existe! Utilize a função get_instance()")

    @classmethod
    async def get_instance(cls):
        """
        Pega o client do cloud storage
        """

        if cls.__instance is None:
            cls.__instance = cls()
            await cls.__instance.create_client()

        return cls.__instance

    @abstractmethod
    async def create_client(self) -> None:
        """
        Realiza a instanciação do storage de acordo com o cloud.
        """

        pass

    @abstractmethod
    async def upload_from_string(self, path: str, content: str, content_type: str, timeout: int) -> Any:
        """
        Insere um documento no bucket.
        """

        pass

    @abstractmethod
    async def list_blobs(self, path: str) -> List[str]:
        """
        Lista todos os arquivos em um caminho específico.
        """

        pass
