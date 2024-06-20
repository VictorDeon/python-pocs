from abc import ABC, abstractmethod
from src.infrastructure.databases.models import User, Company


class CompanyDAOInterface(ABC):
    """
    Interface de criação do repositorio de empresas.
    """

    @abstractmethod
    async def create(
        self,
        cnpj: str,
        name: str,
        fantasy_name: str,
        user: User,
        employees: list[User]) -> Company:
        """
        Cria o grupo passando como argumento os dados do mesmo.
        """
