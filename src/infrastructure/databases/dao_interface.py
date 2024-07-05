from typing import TypeVar, Generic, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.logger import ProjectLoggerSingleton

INPUT = TypeVar("INPUT")
DB_MODEL = TypeVar("DB_MODEL")


class DAOInterface(Generic[INPUT, DB_MODEL]):
    """
    Interface de CRUD
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def create(self, dto: INPUT, commit: bool = True) -> DB_MODEL:
        """
        Cria um objeto.
        """

    async def list(self, dto: INPUT) -> list[DB_MODEL]:
        """
        Pega uma lista de objetos.
        """

    async def get_by_id(self, _id: int) -> Optional[DB_MODEL]:
        """
        Pega os dados de um objeto pelo _id
        """

    async def retrieve(self, dto: INPUT) -> Optional[DB_MODEL]:
        """
        Pega os dados de um objeto por um campo qualquer da modelo.
        """

    async def update(self, _id: int, dto: INPUT, commit: bool = True) -> DB_MODEL:
        """
        Atualiza os dados de um objeto.
        """

    async def delete(self, _id: int, commit: bool = True) -> None:
        """
        Deleta um objeto.
        """

    async def count(self) -> int:
        """
        Pega o total de objetos.
        """
