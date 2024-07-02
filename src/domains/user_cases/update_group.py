from src.adapters import PresenterInterface
from src.adapters.dtos import UpdateGroupInputDTO, UpdateGroupOutputDTO
from src.domains import UserCaseInterface
from src.infrastructure.databases.models import Group
from src.infrastructure.databases import DAOInterface


class UpdateGroupUserCase(UserCaseInterface):
    """
    Caso de uso de atualização de grupos.
    """

    def __init__(
        self,
        presenter: PresenterInterface[Group, UpdateGroupOutputDTO],
        repository: DAOInterface[UpdateGroupInputDTO, Group]):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, _id: int, input_dto: UpdateGroupInputDTO) -> UpdateGroupOutputDTO:
        """
        Executa o caso de uso.
        """

        model = await self.repository.update(_id, dto=input_dto)
        return self.presenter.present(model)
