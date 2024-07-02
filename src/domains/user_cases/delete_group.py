from src.domains import UserCaseInterface
from src.infrastructure.databases.models import Group
from src.infrastructure.databases import DAOInterface


class DeleteGroupUserCase(UserCaseInterface):
    """
    Caso de uso de deleção de grupos.
    """

    def __init__(self, repository: DAOInterface[int, Group]):
        """
        Constructor.
        """

        self.repository = repository

    async def execute(self, _id: int) -> int:
        """
        Executa o caso de uso.
        """

        return await self.repository.delete(_id)
