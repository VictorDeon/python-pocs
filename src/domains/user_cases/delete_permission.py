from src.adapters import PresenterInterface
from src.domains import UserCaseInterface
from src.infrastructure.databases.models import Permission
from src.infrastructure.databases import DAOInterface


class DeletePermissionUserCase(UserCaseInterface):
    """
    Caso de uso de deleção de permissões.
    """

    def __init__(
        self,
        presenter: PresenterInterface[Permission, int],
        repository: DAOInterface[int, Permission]):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, _id: int) -> int:
        """
        Executa o caso de uso.
        """

        return await self.repository.delete(_id=_id)
