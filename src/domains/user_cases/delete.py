from src.domains import UserCaseInterface
from src.infrastructure.databases import DAOInterface


class DeleteUserCase(UserCaseInterface):
    """
    Caso de uso de deleção de um objeto.
    """

    def __init__(self, repository: DAOInterface):
        """
        Constructor.
        """

        self.repository = repository

    async def execute(self, _id: int) -> int:
        """
        Executa o caso de uso.
        """

        return await self.repository.delete(_id=_id)
