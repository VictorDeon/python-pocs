from typing import Any
from src.adapters import PresenterInterface
from src.domains import UserCaseInterface
from src.infrastructure.databases import DAOInterface


class RetrieveUserCase(UserCaseInterface):
    """
    Caso de uso de busca de um objeto.
    """

    def __init__(self, presenter: PresenterInterface, repository: DAOInterface):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: Any) -> Any:
        """
        Executa o caso de uso.
        """

        model = await self.repository.retrieve(dto=input_dto)
        return self.presenter.present(model)
