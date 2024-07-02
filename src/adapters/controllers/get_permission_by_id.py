from src.adapters import ControllerInterface
from src.domains.user_cases import GetByIdUserCase
from src.infrastructure.databases.daos import PermissionDAO
from src.infrastructure.databases import DBConnectionHandler


class GetPermissionByIdController(ControllerInterface):
    """
    Controladora de busca de permissões pelo id
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
            use_case = GetByIdUserCase(repository=repository)
            return await use_case.execute(self.id)
