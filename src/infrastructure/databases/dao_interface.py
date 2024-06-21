from typing import TypeVar, Generic, Optional, AsyncIterator, Any

INPUT = TypeVar("INPUT")
DB_MODEL = TypeVar("DB_MODEL")


class DAOInterface(Generic[INPUT, DB_MODEL]):
    """
    Interface de CRUD
    """

    async def create(self, dto: INPUT) -> DB_MODEL:
        """
        Cria um objeto.
        """

    async def list(self) -> AsyncIterator[DB_MODEL]:
        """
        Pega uma lista de objetos.
        """

    async def retrieve(self, id: int) -> Optional[DB_MODEL]:
        """
        Pega os dados de um objeto pelo _id
        """

    async def update(self, instance: DB_MODEL, dto: INPUT) -> DB_MODEL:
        """
        Atualiza os dados de um objeto.
        """

    async def delete(self, instance: DB_MODEL) -> None:
        """
        Deleta um objeto.
        """

    async def count(self) -> int:
        """
        Pega o total de objetos.
        """
