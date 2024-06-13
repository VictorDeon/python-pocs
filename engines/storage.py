from google.cloud.storage import Client
import os


class StorageSingleton:
    """
    Faz a instrumentalização do google storage.
    """

    __instance = None

    def __init__(self):
        """
        Construtor do cliente.
        """

        if self.__instance is not None:
            raise RuntimeError("A instância do cloud storage já existe! Utilize a função get_client()")

        self.client = Client(project=os.environ.get('GOOGLE_CLOUD_PROJECT'))
        self.bucket = self.client.get_bucket(os.environ.get('BUCKET_NAME'))

    @classmethod
    def get_client(cls):
        """
        Pega o client do cloud storage
        """

        if cls.__instance is None:
            cls.__instance = StorageSingleton()

        return cls.__instance.client

    @classmethod
    def get_bucket(cls):
        """
        Pega o bucket do cloud storage
        """

        if cls.__instance is None:
            cls.__instance = StorageSingleton()

        return cls.__instance.bucket
