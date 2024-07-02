from src.adapters import PresenterInterface
from src.adapters.dtos import ListPermissionInputDTO, ListPermissionOutputDTO
from src.domains import UserCaseInterface
from src.infrastructure.databases.models import Permission
from src.infrastructure.databases import DAOInterface


class ListPermissionUserCase(UserCaseInterface):
    """
    Caso de uso de listagem de permissões.
    """

    def __init__(
        self,
        presenter: PresenterInterface[Permission, ListPermissionOutputDTO],
        repository: DAOInterface[ListPermissionInputDTO, Permission]):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: ListPermissionInputDTO) -> ListPermissionOutputDTO:
        """
        Executa o caso de uso.
        """

        model = await self.repository.list(dto=input_dto)
        return self.presenter.present(model)
