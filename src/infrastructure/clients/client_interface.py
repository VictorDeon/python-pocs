from abc import ABC, abstractmethod


class HttpClientInterface(ABC):
    """
    Cliente de conexão http.
    """

    def __init__(self):
        """
        Constructor.
        """

        self.client = None

    @abstractmethod
    async def __aenter__(self) -> None:
        """
        Iniciando o poll de conexões.
        """

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Fecha o poll de conexões.
        """

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
