from typing import Any
from src.adapters import PresenterInterface
from src.domains import UserCaseInterface
from src.infrastructure.databases import DAOInterface


class CreateUserCase(UserCaseInterface):
    """
    Caso de uso de criação de objetos.
    """

    def __init__(self, presenter: PresenterInterface, repository: DAOInterface) -> None:
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: Any) -> Any:
        """
        Executa o caso de uso.
        """

        model = await self.repository.create(dto=input_dto)
        return self.presenter.present(model)
