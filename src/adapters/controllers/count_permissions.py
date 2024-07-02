from src.adapters import ControllerInterface
from src.domains.user_cases import CountUserCase
from src.infrastructure.databases.daos import PermissionDAO
from src.infrastructure.databases import DBConnectionHandler


class CountPermissionController(ControllerInterface):
    """
    Controladora de contagem de permissões
    """

    async def execute(self) -> int:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = PermissionDAO(session=session)
            use_case = CountUserCase(repository=repository)
            return await use_case.execute()
