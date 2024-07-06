from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.error import ErrorPresenter
from ..dtos import RetrievePermissionOutputDTO
from ..models import Permission


class RetrievePermissionPresenter:
    """
    Formatação de saída da API que buscar uma permissão.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, model: Permission) -> RetrievePermissionOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        if not model:
            return await ErrorPresenter(session=self.session).present(
                message="Permissão não encontrada.",
            )

        return RetrievePermissionOutputDTO(
            id=model.id,
            name=model.name,
            code=model.code
        )
