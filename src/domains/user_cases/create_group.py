from src.adapters import PresenterInterface
from src.adapters.dtos import CreateGroupInputDTO, CreateGroupOutputDTO
from src.domains import UserCaseInterface
from src.infrastructure.databases.models import Group
from src.infrastructure.databases import DAOInterface


class CreateGroupUserCase(UserCaseInterface):
    """
    Caso de uso de criação de grupos.
    """

    def __init__(
        self,
        presenter: PresenterInterface[Group, CreateGroupOutputDTO],
        repository: DAOInterface[CreateGroupInputDTO, Group]):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: CreateGroupInputDTO) -> CreateGroupOutputDTO:
        """
        Executa o caso de uso.
        """

        model = await self.repository.create(dto=input_dto)
        return self.presenter.present(model)
