from sqlalchemy.ext.asyncio import AsyncSession
from .retrieve import RetrievePermissionPresenter
from ..models import Permission
from ..dtos import UpdatePermissionOutputDTO


class UpdatePermissionPresenter(PresenterInterface):
    """
    Formatação de saída da API que atualizar uma permissão.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, model: Permission) -> UpdatePermissionOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        permission = await RetrievePermissionPresenter(session=self.session).present(model)
        return UpdatePermissionOutputDTO(**permission.to_dict())
