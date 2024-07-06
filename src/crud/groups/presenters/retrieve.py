from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.permissions.models import Permission
from src.crud.permissions.presenters import ListPermissionPresenter
from src.crud.permissions.dtos import ListPermissionInputDTO
from src.crud.permissions.repositories import ListPermissionDAO
from src.shared.error import ErrorPresenter
from ..dtos import RetrieveGroupOutputDTO
from ..models import Group


class RetrieveGroupPresenter:
    """
    Formatação de saída da API que buscar um grupo.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, model: Group) -> RetrieveGroupOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        if not model:
            return await ErrorPresenter(session=self.session).present(
                message="Grupo não encontrado.",
            )

        permission_dao = ListPermissionDAO(session=self.session)
        permissions: list[Permission] = await permission_dao.list(dto=ListPermissionInputDTO(group_id=model.id))
        permission_presenter = ListPermissionPresenter(session=self.session)
        permissions = await permission_presenter.present(permissions)

        return RetrieveGroupOutputDTO(
            id=model.id,
            name=model.name,
            permissions=permissions
        )
