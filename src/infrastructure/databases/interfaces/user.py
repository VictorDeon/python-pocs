from abc import ABC, abstractmethod
from src.domains.entities import User
from src.infrastructure.databases.models import (
    Group as GroupModel,
    Permission as PermissionModel,
    Company as CompanyModel
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
        work_company: CompanyModel = None,
        groups: list[GroupModel] = [],
        permissions: list[PermissionModel] = []) -> User:
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
