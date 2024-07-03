from src.adapters import ControllerInterface
from src.adapters.dtos import CreateGroupInputDTO, CreateGroupOutputDTO
from src.adapters.presenters import CreateGroupPresenter
from src.domains.user_cases import CreateUserCase
from src.infrastructure.databases.daos import GroupDAO
from src.infrastructure.databases import DBConnectionHandler


class CreateGroupController(ControllerInterface):
    """
    Controladora de criação de grupos
    """

    def __init__(self, input: CreateGroupInputDTO):
        """
        Construtor.
        """

        self.input = input

    async def execute(self) -> CreateGroupOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = GroupDAO(session=session)
            output = CreateGroupPresenter(session=session)
            use_case = CreateUserCase(
                presenter=output,
                repository=repository
            )
            return await use_case.execute(self.input)
