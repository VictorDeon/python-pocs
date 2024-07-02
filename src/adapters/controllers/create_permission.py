from src.adapters import ControllerInterface
from src.adapters.dtos import CreatePermissionInputDTO, CreatePermissionOutputDTO
from src.adapters.presenters import CreatePermissionPresenter
from src.domains.user_cases import CreateUserCase
from src.infrastructure.databases.daos import PermissionDAO
from src.infrastructure.databases import DBConnectionHandler


class CreatePermissionController(ControllerInterface):
    """
    Controladora de criação de permissões
    """

    def __init__(self, input: CreatePermissionInputDTO):
        """
        Construtor.
        """

        self.input = input

    async def execute(self) -> CreatePermissionOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = PermissionDAO(session=session)
            output = CreatePermissionPresenter(session=session)
            use_case = CreateUserCase(
                presenter=output,
                repository=repository
            )
            return await use_case.execute(self.input)
