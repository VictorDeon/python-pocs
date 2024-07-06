from io import TextIOWrapper
from typing import List


class LocalStorageSingleton:
    """
    Faz a instrumentalização do storage local.
    """

    __instance = None

    def __init__(self) -> None:
        """
        Construtor do cliente.
        """

        if self.__instance is not None:
            raise RuntimeError("A instância do storage já existe! Utilize a função get_instance()")

        self.client = None
        self.bucket = None

    @classmethod
    async def get_instance(cls):
        """
        Pega o client do cloud storage
        """

        if cls.__instance is None:
            cls.__instance = LocalStorageSingleton()

        return cls.__instance

    async def upload_from_string(self, path: str, content: str, content_type: str, timeout: int) -> TextIOWrapper:
        """
        Insere um documento no bucket do GCP.
        """

        with open(path, "wb") as file:
            file.write(content)

        return file

    async def list_blobs(self, path: str) -> List[str]:
        """
        Lista todos os arquivos de uma caminho específico.
        """

        return []
