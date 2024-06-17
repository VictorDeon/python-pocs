from io import TextIOWrapper
from typing import List
from ..storage_interface import StorageSingletonInterface


class LocalStorageSingleton(StorageSingletonInterface):
    """
    Faz a instrumentalização do storage local.
    """

    async def create_client(self) -> None:
        """
        Realiza a instanciação do storage do google cloud plataform (GCP).
        """

        pass

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
