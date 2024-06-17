from src.adapters.interfaces import ControllerInterface
from src.adapters.dtos import FindUserInputDTO
from src.infrastructure.databases.daos import UserDAO
from src.adapters.presenters import FindUserPresenter
from src.domains.user_cases import UserRetrieve


class UserRetrieveController(ControllerInterface):
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
        use_case = UserRetrieve(output, repository)
        return await use_case.execute(self.input)
