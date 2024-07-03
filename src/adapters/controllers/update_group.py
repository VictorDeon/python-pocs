from src.adapters import ControllerInterface
from src.adapters.dtos import UpdateGroupInputDTO, UpdateGroupOutputDTO
from src.adapters.presenters import UpdateGroupPresenter
from src.domains.user_cases import UpdateUserCase
from src.infrastructure.databases.daos import GroupDAO
from src.infrastructure.databases import DBConnectionHandler


class UpdateGroupController(ControllerInterface):
    """
    Controladora de atualização de grupos
    """

    def __init__(self, _id: int, input: UpdateGroupInputDTO):
        """
        Construtor.
        """

        self.input = input
        self.id = _id

    async def execute(self) -> UpdateGroupOutputDTO:
        """
        Lida com a entrada e saida dos dados.
        """

        async with DBConnectionHandler() as session:
            repository = GroupDAO(session=session)
            output = UpdateGroupPresenter(session=session)
            use_case = UpdateUserCase(
                presenter=output,
                repository=repository
            )
            return await use_case.execute(self.id, self.input)
