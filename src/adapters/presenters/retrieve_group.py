from src.adapters.dtos import ListPermissionInputDTO, RetrieveGroupOutputDTO
from src.adapters import PresenterInterface
from src.domains.entities import Group
from src.infrastructure.databases.models import (
    Group as GroupModel,
    Permission as PermissionModel
)
from src.infrastructure.databases.daos import PermissionDAO
from .list_permissions import ListPermissionPresenter
from .error import ErrorPresenter


class RetrieveGroupPresenter(PresenterInterface):
    """
    Formatação de saída da API que buscar um grupo.
    """

    async def present(self, model: GroupModel) -> RetrieveGroupOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        if not model:
            return await ErrorPresenter(session=self.session).present(
                message="Grupo não encontrado.",
            )

        permission_dao = PermissionDAO(session=self.session)
        permissions: list[PermissionModel] = await permission_dao.list(dto=ListPermissionInputDTO(group_id=model.id))
        permission_presenter = ListPermissionPresenter(session=self.session)
        presenter = await permission_presenter.present(permissions)

        group = Group(
            id=model.id,
            name=model.name,
            permissions=presenter.permissions
        )

        return RetrieveGroupOutputDTO(group=group)
