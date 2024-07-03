from src.adapters import ControllerInterface
from src.adapters.dtos import UpdateUserInputDTO, UpdateUserOutputDTO
from src.adapters.presenters import UpdateUserPresenter
from src.domains.user_cases import UpdateUserCase
from src.infrastructure.databases.daos import UserDAO
from src.infrastructure.databases import DBConnectionHandler


class UpdateUserController(ControllerInterface):
    """
    Controladora de atualização de usuários
    """

    def __init__(self, _id: int, input: UpdateUserInputDTO):
        """
        Construtor.
        """

        self.input = input
        self.id = _id

    async def execute(self) -> UpdateUserOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = UserDAO(session=session)
            output = UpdateUserPresenter(session=session)
            use_case = UpdateUserCase(
                presenter=output,
                repository=repository
            )
            return await use_case.execute(self.id, self.input)
