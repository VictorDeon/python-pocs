from src.adapters.interfaces import ControllerInterface
from src.adapters.dtos import FindUserInputDTO
from src.adapters.presenters import FindUserPresenter
from src.domains.user_cases import FindUser
from src.infrastructure.databases.daos import UserDAO


class FindUserController(ControllerInterface):
    """
    Controladora de acesso externo para buscar os dados de uma API.
    """

    def __init__(self, user_id: int):
        """
        Construtor.
        """

        self.input = FindUserInputDTO(id=user_id)

    async def execute(self) -> dict:
        """
        Lida com a entrada e saida dos dados.
        """

        repository = UserDAO()
        output = FindUserPresenter()
        use_case = FindUser(output, repository)
        return await use_case.execute(self.input)
