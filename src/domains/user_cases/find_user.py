from src.adapters import PresenterInterface
from src.adapters.presenters import FindUserPresenter
from src.adapters.dtos import FindUserInputDTO, FindUserOutputDTO
from src.domains import UserCaseInterface
from src.infrastructure.databases.daos import UserDAO
from src.infrastructure.databases import DAOInterface


class FindUser(UserCaseInterface):
    """
    Caso de uso de procura de um usuários.
    """

    def __init__(
        self,
        presenter: PresenterInterface[FindUserPresenter],
        repository: DAOInterface[UserDAO]):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: FindUserInputDTO) -> FindUserOutputDTO:
        """
        Encontra o usuário pelo email.
        """

        user = await self.repository.retrieve(input_dto.id)
        return self.presenter.present(user)
