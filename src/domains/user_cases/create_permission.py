from src.adapters import PresenterInterface
from src.adapters.dtos import CreatePermissionInputDTO, CreatePermissionOutputDTO
from src.domains import UserCaseInterface
from src.infrastructure.databases.models import Permission
from src.infrastructure.databases import DAOInterface


class CreatePermissionUserCase(UserCaseInterface):
    """
    Caso de uso de criação de permissões.
    """

    def __init__(
        self,
        presenter: PresenterInterface[Permission, CreatePermissionOutputDTO],
        repository: DAOInterface[CreatePermissionInputDTO, Permission]):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: CreatePermissionInputDTO) -> CreatePermissionOutputDTO:
        """
        Executa o caso de uso.
        """

        model = await self.repository.create(dto=input_dto)
        return self.presenter.present(model)
