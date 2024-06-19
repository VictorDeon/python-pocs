from abc import ABC, abstractmethod
from src.domains.entities import Permission


class PermissionDAOInterface(ABC):
    """
    Interface de criação do repositorio de permissões.
    """

    @abstractmethod
    async def create(self, name: str) -> Permission:
        """
        Cria a permissão passando como argumento os dados do mesmo.
        """
