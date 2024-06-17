from abc import ABC, abstractmethod


class HttpClientSingletonInterface(ABC):

    __instance = None

    def __init__(self):
        """
        Construtor.
        """

        if self.__instance is not None:
            raise RuntimeError("A instância do http client já existe. Utilize o método get_instance().")

    @classmethod
    def get_instance(cls):
        """
        Pega a instância do cliente http.
        """

        if cls.__instance is None:
            cls.__instance = cls()
            cls.__instance.start_connection()

        return cls.__instance

    @abstractmethod
    def start_connection(self) -> None:
        """
        Iniciando o poll de conexões.
        """

        pass

    @abstractmethod
    async def get(self, url: str, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo GET.
        """

        pass

    @abstractmethod
    async def post(self, url: str, data: dict, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo POST.
        """

        pass

    @abstractmethod
    async def put(self, url: str, data: dict, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo PUT.
        """

        pass

    @abstractmethod
    async def patch(self, url: str, data: dict, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo PATCH.
        """

        pass

    @abstractmethod
    async def delete(self, url: str, params: dict = None, headers: dict = None, timeout: int = 600) -> dict:
        """
        Realiza requisição do tipo DELETE.
        """

        pass

    @abstractmethod
    async def close_connection(self) -> None:
        """
        Fecha a conexão.
        """

        pass
