from typing import Any
from src.adapters import PresenterInterface
from src.domains import UserCaseInterface
from src.infrastructure.databases import DAOInterface


class UpdateUserCase(UserCaseInterface):
    """
    Caso de uso de atualização de objetos.
    """

    def __init__(self, presenter: PresenterInterface, repository: DAOInterface):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, _id: int, input_dto: Any) -> Any:
        """
        Executa o caso de uso.
        """

        model = await self.repository.update(_id, dto=input_dto)
        return self.presenter.present(model)
