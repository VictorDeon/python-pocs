from src.adapters import ControllerInterface
from src.adapters.dtos import UpdatePermissionInputDTO, UpdatePermissionOutputDTO
from src.adapters.presenters import UpdatePermissionPresenter
from src.domains.user_cases import UpdateUserCase
from src.infrastructure.databases.daos import PermissionDAO
from src.infrastructure.databases import DBConnectionHandler


class UpdatePermissionController(ControllerInterface):
    """
    Controladora de atualização de permissões
    """

    def __init__(self, input: UpdatePermissionInputDTO):
        """
        Construtor.
        """

        self.input = input

    async def execute(self) -> UpdatePermissionOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = PermissionDAO(session=session)
            output = UpdatePermissionPresenter(session=session)
            use_case = UpdateUserCase(
                presenter=output,
                repository=repository
            )
            return await use_case.execute(self.input)
