from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Permission
from ..dtos import CreatePermissionOutputDTO
from .retrieve import RetrievePermissionPresenter


class CreatePermissionPresenter:
    """
    Formatação de saída da API que cria uma permissão.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, model: Permission) -> CreatePermissionOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        permission = await RetrievePermissionPresenter(session=self.session).present(model)
        return CreatePermissionOutputDTO(**permission.to_dict())
