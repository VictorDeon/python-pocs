from src.adapters import ControllerInterface
from src.domains.user_cases import DeleteUserCase
from src.infrastructure.databases.daos import PermissionDAO
from src.infrastructure.databases import DBConnectionHandler


class DeletePermissionController(ControllerInterface):
    """
    Controladora de deleção de permissões
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
            repository = PermissionDAO(session=session)
            use_case = DeleteUserCase(repository=repository)
            return await use_case.execute(self.id)
