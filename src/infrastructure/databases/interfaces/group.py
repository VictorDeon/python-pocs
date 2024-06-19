from typing import List
from abc import ABC, abstractmethod
from src.infrastructure.databases.models import Permission as PermissionModel
from src.domains.entities import Group


class GroupDAOInterface(ABC):
    """
    Interface de criação do repositorio de grupos.
    """

    @abstractmethod
    async def create(self, name: str, permissions: List[PermissionModel]) -> Group:
        """
        Cria o grupo passando como argumento os dados do mesmo.
        """
