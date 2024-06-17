from src.domains.interfaces import UserCaseInterface
from src.infrastructure.databases.interfaces import UserDAOInterface
from src.adapters.interfaces import PresenterInterface
from src.adapters.dtos import FindUserInputDTO, FindUserOutputDTO


class UserRetrieve(UserCaseInterface):
    """
    Caso de uso de procura de um usuários.
    """

    def __init__(self, presenter: PresenterInterface, repository: UserDAOInterface):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: FindUserInputDTO) -> dict:
        """
        Encontra o usuário pelo email.
        """

        user = await self.repository.retrieve(input_dto.id)
        output_dto = FindUserOutputDTO(user=user)
        return self.presenter.present(output_dto)
