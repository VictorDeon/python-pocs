from typing import TypeVar, Generic, Optional
from sqlalchemy.ext.asyncio import AsyncSession

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

    async def create(self, dto: INPUT, commit: bool = True, close_session: bool = True) -> DB_MODEL:
        """
        Cria um objeto.
        """

    async def list(self, dto: INPUT, close_session: bool = True) -> list[DB_MODEL]:
        """
        Pega uma lista de objetos.
        """

    async def get_by_id(self, _id: int, close_session: bool = True) -> Optional[DB_MODEL]:
        """
        Pega os dados de um objeto pelo _id
        """

    async def retrieve(self, dto: INPUT, close_session: bool = True) -> Optional[DB_MODEL]:
        """
        Pega os dados de um objeto por um campo qualquer da modelo.
        """

    async def update(self, _id: int, dto: INPUT, commit: bool = True, close_session: bool = True) -> DB_MODEL:
        """
        Atualiza os dados de um objeto.
        """

    async def delete(self, _id: int, commit: bool = True, close_session: bool = True) -> None:
        """
        Deleta um objeto.
        """

    async def count(self, close_session: bool = True) -> int:
        """
        Pega o total de objetos.
        """
