from src.adapters.interfaces import PresenterInterface
from src.adapters.presenters import CreatePermissionPresenter
from src.adapters.dtos import CreatePermissionInputDTO, CreatePermissionOutputDTO
from src.domains.interfaces import UserCaseInterface
from src.infrastructure.databases.daos import PermissionDAO
from src.infrastructure.databases import DAOInterface


class CreatePermission(UserCaseInterface[CreatePermissionInputDTO, CreatePermissionOutputDTO]):
    """
    Caso de uso de criação de permissões.
    """

    def __init__(
        self,
        presenter: PresenterInterface[CreatePermissionPresenter],
        repository: DAOInterface[PermissionDAO]):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: CreatePermissionInputDTO) -> CreatePermissionOutputDTO:
        """
        Executa o caso de uso.
        """

        user = await self.repository.create(dto=input_dto)
        return self.presenter.present(user)
