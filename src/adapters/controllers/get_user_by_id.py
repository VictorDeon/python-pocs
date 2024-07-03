from src.adapters import ControllerInterface
from src.adapters.presenters import RetrieveUserPresenter
from src.domains.user_cases import GetByIdUserCase
from src.infrastructure.databases.daos import UserDAO
from src.infrastructure.databases import DBConnectionHandler


class GetUserByIdController(ControllerInterface):
    """
    Controladora de busca de usuários pelo id
    """

    def __init__(self, _id: int):
        """
        Construtor.
        """

        self.id = _id

    async def execute(self) -> int:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = UserDAO(session=session)
            presenter = RetrieveUserPresenter(session=session)
            use_case = GetByIdUserCase(
                presenter=presenter,
                repository=repository
            )
            return await use_case.execute(self.id)
