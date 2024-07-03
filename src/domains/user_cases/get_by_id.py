from typing import Any, Union
from src.adapters import PresenterInterface
from src.domains import UserCaseInterface
from src.infrastructure.databases import DAOInterface


class GetByIdUserCase(UserCaseInterface):
    """
    Caso de uso de busca de um objeto pelo id.
    """

    def __init__(self, presenter: PresenterInterface, repository: DAOInterface):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, _id: Union[int, str]) -> Any:
        """
        Executa o caso de uso.
        """

        model = await self.repository.get_by_id(_id)
        return self.presenter.present(model)
