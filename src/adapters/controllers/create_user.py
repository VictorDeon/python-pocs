from src.adapters import ControllerInterface
from src.adapters.dtos import CreateUserInputDTO, CreateUserOutputDTO
from src.adapters.presenters import CreateUserPresenter
from src.domains.user_cases import CreateUserCase
from src.infrastructure.databases.daos import UserDAO
from src.infrastructure.databases import DBConnectionHandler


class CreateUserController(ControllerInterface):
    """
    Controladora de criação de usuários
    """

    def __init__(self, input: CreateUserInputDTO):
        """
        Construtor.
        """

        self.input = input

    async def execute(self) -> CreateUserOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = UserDAO(session=session)
            output = CreateUserPresenter(session=session)
            use_case = CreateUserCase(
                presenter=output,
                repository=repository
            )
            return await use_case.execute(self.input)
