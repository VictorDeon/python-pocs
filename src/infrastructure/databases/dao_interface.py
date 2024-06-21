from typing import TypeVar, Generic, Optional, AsyncIterator, Any

T = TypeVar("T")


class DAOInterface(Generic[T]):
    """
    Interface de CRUD
    """

    async def create(self, dto: Any) -> Any:
        """
        Cria um objeto.
        """

    async def list(self) -> AsyncIterator[Any]:
        """
        Pega uma lista de objetos.
        """

    async def retrieve(self, id: int) -> Optional[Any]:
        """
        Pega os dados de um objeto pelo _id
        """

    async def update(self, instance: Any, dto: Any) -> Any:
        """
        Atualiza os dados de um objeto.
        """

    async def delete(self, instance: Any) -> None:
        """
        Deleta um objeto.
        """

    async def count(self) -> int:
        """
        Pega o total de objetos.
        """
