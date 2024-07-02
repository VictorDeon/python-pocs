from src.adapters import PresenterInterface
from src.adapters.dtos import ListGroupInputDTO, ListGroupOutputDTO
from src.domains import UserCaseInterface
from src.infrastructure.databases.models import Group
from src.infrastructure.databases import DAOInterface


class ListGroupUserCase(UserCaseInterface):
    """
    Caso de uso de listagem de grupos.
    """

    def __init__(
        self,
        presenter: PresenterInterface[list[Group], ListGroupOutputDTO],
        repository: DAOInterface[ListGroupInputDTO, list[Group]]):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: ListGroupInputDTO) -> ListGroupOutputDTO:
        """
        Executa o caso de uso.
        """

        models = await self.repository.list(dto=input_dto)
        return self.presenter.present(models)
