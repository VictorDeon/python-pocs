from google.cloud.storage import Client, Blob, Bucket
from asyncer import asyncify
from typing import List
from src.infrastructure.storage import StorageSingletonInterface
import os


class GCPStorageSingleton(StorageSingletonInterface):
    """
    Faz a instrumentalização do google storage.
    """

    async def create_client(self) -> None:
        """
        Realiza a instanciação do storage do google cloud plataform (GCP).
        """

        self.client = Client(project=os.environ.get('CLOUD_PROJECT'))
        self.bucket: Bucket = self.client.get_bucket(os.environ.get('BUCKET_NAME'))

    async def upload_from_string(self, path: str, string_content: str, content_type: str, timeout: int) -> Blob:
        """
        Insere um documento no bucket do GCP.
        """

        blob = Blob(path, self.bucket)
        await asyncify(blob.upload_from_string)(string_content, content_type=content_type, timeout=timeout)
        return blob

    async def list_blobs(self, path: str) -> List[str]:
        """
        Lista todos os arquivos de uma caminho específico.
        """

        return []
