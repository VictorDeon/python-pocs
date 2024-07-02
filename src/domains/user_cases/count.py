from src.domains import UserCaseInterface
from src.infrastructure.databases import DAOInterface


class CountUserCase(UserCaseInterface):
    """
    Caso de uso de contagem de objetos.
    """

    def __init__(self, repository: DAOInterface):
        """
        Constructor.
        """

        self.repository = repository

    async def execute(self) -> int:
        """
        Executa o caso de uso.
        """

        return await self.repository.count()
