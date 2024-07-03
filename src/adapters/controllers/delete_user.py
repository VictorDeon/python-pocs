from src.adapters import ControllerInterface
from src.domains.user_cases import DeleteUserCase
from src.infrastructure.databases.daos import UserDAO
from src.infrastructure.databases import DBConnectionHandler


class DeleteUserController(ControllerInterface):
    """
    Controladora de deleção de usuários
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
            use_case = DeleteUserCase(repository=repository)
            return await use_case.execute(self.id)
