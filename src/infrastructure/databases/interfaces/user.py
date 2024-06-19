from abc import ABC, abstractmethod
from src.domains.entities import User


class UserDAOInterface(ABC):
    """
    Interface de criação do repositorio de usuários.
    """

    @abstractmethod
    async def create(self, email: str, name: str, password: str) -> User:
        """
        Cria o usuário passando como argumento os dados do mesmo.
        """

    @abstractmethod
    async def retrieve(self, _id: int) -> User:
        """
        Pesquisa o usuário pelo email.
        """

    @abstractmethod
    async def list(self, email: str = None) -> list[User]:
        """
        Pesquisa o usuário pelo email.
        """
