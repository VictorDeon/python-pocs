from abc import ABC, abstractmethod
from src.infrastructure.databases.models import (
    Group,
    Permission,
    Company,
    User
)


class UserDAOInterface(ABC):
    """
    Interface de criação do repositorio de usuários.
    """

    @abstractmethod
    async def create(
        self,
        email: str,
        name: str,
        password: str,
        phone: str = None,
        address: str = None,
        work_company: Company = None,
        groups: list[Group] = [],
        permissions: list[Permission] = []) -> User:
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
