from src.adapters import ControllerInterface
from src.adapters.dtos import CreatePermissionInputDTO, CreatePermissionOutputDTO
from src.adapters.presenters import CreatePermissionPresenter
from src.domains.user_cases import CreatePermissionUserCase
from src.infrastructure.databases.daos import PermissionDAO


class CreatePermissionController(ControllerInterface):
    """
    Controladora de acesso externo para buscar os dados de uma API.
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

        repository = PermissionDAO()
        output = CreatePermissionPresenter()
        use_case = CreatePermissionUserCase(output, repository)
        return await use_case.execute(self.input)
