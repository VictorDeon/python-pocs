from abc import ABC, abstractmethod
from typing import Any
from src.infrastructure.databases.models import Permission


class PermissionDAOInterface(ABC):
    """
    Interface de criação do repositorio de permissões.
    """

    @abstractmethod
    async def create(self, dto: Any) -> Permission:
        """
        Cria a permissão passando como argumento os dados do mesmo.
        """
