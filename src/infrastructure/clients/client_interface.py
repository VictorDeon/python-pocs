from abc import ABC, abstractmethod
import httpx


class HttpClientSingletonInterface(ABC):

    __instance = None

    def __init__(self):
        """
        Construtor.
        """

        if self.__instance is not None:
            raise RuntimeError("A instância do http client já existe. Utilize o método get_instance().")

        self.client = httpx.AsyncClient()

    @classmethod
    def get_instance(cls):
        """
        Pega a instância do cliente http.
        """

        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    @abstractmethod
    async def get(self, url: str, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo GET.
        """

    @abstractmethod
    async def post(self, url: str, data: dict, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo POST.
        """

    @abstractmethod
    async def put(self, url: str, data: dict, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo PUT.
        """

    @abstractmethod
    async def patch(self, url: str, data: dict, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo PATCH.
        """

    @abstractmethod
    async def delete(self, url: str, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo DELETE.
        """
