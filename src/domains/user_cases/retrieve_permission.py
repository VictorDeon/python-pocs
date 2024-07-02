from src.adapters import PresenterInterface
from src.adapters.dtos import RetrievePermissionInputDTO, RetrievePermissionOutputDTO
from src.domains import UserCaseInterface
from src.infrastructure.databases.models import Permission
from src.infrastructure.databases import DAOInterface


class RetrievePermissionUserCase(UserCaseInterface):
    """
    Caso de uso de busca de permissões.
    """

    def __init__(
        self,
        presenter: PresenterInterface[Permission, RetrievePermissionOutputDTO],
        repository: DAOInterface[RetrievePermissionInputDTO, Permission]):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: RetrievePermissionInputDTO) -> RetrievePermissionOutputDTO:
        """
        Executa o caso de uso.
        """

        model = await self.repository.retrieve(dto=input_dto)
        return self.presenter.present(model)
