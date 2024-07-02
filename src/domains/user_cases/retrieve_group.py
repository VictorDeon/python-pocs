from src.adapters import PresenterInterface
from src.domains import UserCaseInterface
from src.infrastructure.databases.models import Group
from src.infrastructure.databases import DAOInterface


class RetrieveGroupUserCase(UserCaseInterface):
    """
    Caso de uso de busca de grupos.
    """

    def __init__(
        self,
        presenter: PresenterInterface[Group, Group],
        repository: DAOInterface[int, Group]):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, _id: int) -> Group:
        """
        Executa o caso de uso.
        """

        model = await self.repository.get_by_id(_id=_id)
        return self.presenter.present(model)
