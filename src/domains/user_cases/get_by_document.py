from typing import Any
from src.adapters import PresenterInterface
from src.domains import UserCaseInterface
from src.infrastructure.databases import DAOInterface


class GetByDocumentUserCase(UserCaseInterface):
    """
    Caso de uso de busca de um objeto pelo cpf/cnpj.
    """

    def __init__(self, presenter: PresenterInterface, repository: DAOInterface):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, document: str) -> Any:
        """
        Executa o caso de uso.
        """

        model = await self.repository.retrieve(document)
        return await self.presenter.present(model)
