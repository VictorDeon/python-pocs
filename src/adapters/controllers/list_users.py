from src.adapters import ControllerInterface
from src.adapters.dtos import ListUserInputDTO, ListUserOutputDTO
from src.adapters.presenters import ListUserPresenter
from src.domains.user_cases import ListUserCase
from src.infrastructure.databases.daos import UserDAO
from src.infrastructure.databases import DBConnectionHandler


class ListUsersController(ControllerInterface):
    """
    Controladora de listagem das usuários
    """

    def __init__(self, input: ListUserInputDTO):
        """
        Construtor.
        """

        self.input = input

    async def execute(self) -> ListUserOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = UserDAO(session=session)
            output = ListUserPresenter(session=session)
            use_case = ListUserCase(
                presenter=output,
                repository=repository
            )
            return await use_case.execute(self.input)
