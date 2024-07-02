from src.adapters import ControllerInterface
from src.adapters.dtos import RetrievePermissionInputDTO, RetrievePermissionOutputDTO
from src.adapters.presenters import RetrievePermissionPresenter
from src.domains.user_cases import RetrieveUserCase
from src.infrastructure.databases.daos import PermissionDAO
from src.infrastructure.databases import DBConnectionHandler


class RetrievePermissionController(ControllerInterface):
    """
    Controladora de busca de uma permissão
    """

    def __init__(self, input: RetrievePermissionInputDTO):
        """
        Construtor.
        """

        self.input = input

    async def execute(self) -> RetrievePermissionOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = PermissionDAO(session=session)
            output = RetrievePermissionPresenter(session=session)
            use_case = RetrieveUserCase(
                presenter=output,
                repository=repository
            )
            return await use_case.execute(self.input)
