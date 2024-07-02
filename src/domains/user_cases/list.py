from typing import Any
from src.adapters import PresenterInterface
from src.domains import UserCaseInterface
from src.infrastructure.databases import DAOInterface


class ListUserCase(UserCaseInterface):
    """
    Caso de uso de listagem de objetos.
    """

    def __init__(self, presenter: PresenterInterface, repository: DAOInterface):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: Any) -> list[Any]:
        """
        Executa o caso de uso.
        """

        models = await self.repository.list(dto=input_dto)
        return self.presenter.present(models)
