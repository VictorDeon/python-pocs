from src.adapters import PresenterInterface
from src.adapters.dtos import UpdatePermissionInputDTO, UpdatePermissionOutputDTO
from src.domains import UserCaseInterface
from src.infrastructure.databases.models import Permission
from src.infrastructure.databases import DAOInterface


class UpdatePermissionUserCase(UserCaseInterface):
    """
    Caso de uso de atualização de permissões.
    """

    def __init__(
        self,
        presenter: PresenterInterface[Permission, UpdatePermissionOutputDTO],
        repository: DAOInterface[UpdatePermissionInputDTO, Permission]):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, _id: int, input_dto: UpdatePermissionInputDTO) -> UpdatePermissionOutputDTO:
        """
        Executa o caso de uso.
        """

        model = await self.repository.update(_id=_id, dto=input_dto)
        return self.presenter.present(model)
