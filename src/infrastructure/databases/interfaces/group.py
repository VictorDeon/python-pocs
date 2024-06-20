from abc import ABC, abstractmethod
from src.infrastructure.databases.models import Permission, Group


class GroupDAOInterface(ABC):
    """
    Interface de criação do repositorio de grupos.
    """

    @abstractmethod
    async def create(self, name: str, permissions: list[Permission]) -> Group:
        """
        Cria o grupo passando como argumento os dados do mesmo.
        """
