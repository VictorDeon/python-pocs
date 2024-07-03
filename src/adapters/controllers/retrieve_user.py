from src.adapters import ControllerInterface
from src.adapters.dtos import RetrieveUserInputDTO, RetrieveUserOutputDTO
from src.adapters.presenters import RetrieveUserPresenter
from src.domains.user_cases import RetrieveUserCase
from src.infrastructure.databases.daos import UserDAO
from src.infrastructure.databases import DBConnectionHandler


class RetrieveUserController(ControllerInterface):
    """
    Controladora de busca de uma usuários
    """

    def __init__(self, input: RetrieveUserInputDTO):
        """
        Construtor.
        """

        self.input = input

    async def execute(self) -> RetrieveUserOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = UserDAO(session=session)
            output = RetrieveUserPresenter(session=session)
            use_case = RetrieveUserCase(
                presenter=output,
                repository=repository
            )
            return await use_case.execute(self.input)
