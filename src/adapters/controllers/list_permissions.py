from src.adapters import ControllerInterface
from src.adapters.dtos import ListPermissionInputDTO, ListPermissionOutputDTO
from src.adapters.presenters import ListPermissionPresenter
from src.domains.user_cases import ListUserCase
from src.infrastructure.databases.daos import PermissionDAO
from src.infrastructure.databases import DBConnectionHandler


class ListPermissionsController(ControllerInterface):
    """
    Controladora de listagem das permissões
    """

    def __init__(self, input: ListPermissionInputDTO):
        """
        Construtor.
        """

        self.input = input

    async def execute(self) -> ListPermissionOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = PermissionDAO(session=session)
            output = ListPermissionPresenter(session=session)
            use_case = ListUserCase(
                presenter=output,
                repository=repository
            )
            return await use_case.execute(self.input)
