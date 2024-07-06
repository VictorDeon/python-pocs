import os
from typing import List
from asyncer import asyncify
from google.cloud.storage import Client, Blob, Bucket


class GCPStorageSingleton:
    """
    Faz a instrumentalização do google storage.
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
            cls.__instance = GCPStorageSingleton()
            await cls.__instance.create_client()

        return cls.__instance

    async def create_client(self) -> None:
        """
        Realiza a instanciação do storage do google cloud plataform (GCP).
        """

        self.client = Client(project=os.environ.get('CLOUD_PROJECT'))
        self.bucket: Bucket = self.client.get_bucket(os.environ.get('BUCKET_NAME'))

    async def upload_from_string(self, path: str, content: str, content_type: str, timeout: int) -> Blob:
        """
        Insere um documento no bucket do GCP.
        """

        blob = Blob(path, self.bucket)
        await asyncify(blob.upload_from_string)(content, content_type=content_type, timeout=timeout)
        return blob

    async def list_blobs(self, path: str) -> List[str]:
        """
        Lista todos os arquivos de uma caminho específico.
        """

        return []
