from src.adapters import ControllerInterface
from src.adapters.dtos import ListGroupInputDTO, ListGroupOutputDTO
from src.adapters.presenters import ListGroupPresenter
from src.domains.user_cases import ListUserCase
from src.infrastructure.databases.daos import GroupDAO
from src.infrastructure.databases import DBConnectionHandler


class ListGroupsController(ControllerInterface):
    """
    Controladora de listagem dos grupos
    """

    def __init__(self, input: ListGroupInputDTO):
        """
        Construtor.
        """

        self.input = input

    async def execute(self) -> ListGroupOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = GroupDAO(session=session)
            output = ListGroupPresenter(session=session)
            use_case = ListUserCase(
                presenter=output,
                repository=repository
            )
            return await use_case.execute(self.input)
