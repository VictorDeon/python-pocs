from src.adapters.dtos import ListPermissionInputDTO
from src.adapters import PresenterInterface
from src.domains.entities import Group
from src.infrastructure.databases.models import (
    Group as GroupModel,
    Permission as PermissionModel
)
from src.infrastructure.databases.daos import PermissionDAO
from .list_permissions import ListPermissionPresenter


class RetrieveGroupPresenter(PresenterInterface):
    """
    Formatação de saída da API que buscar um grupo.
    """

    async def present(self, model: GroupModel) -> Group:
        """
        Forma final de apresentação dos dados.
        """

        permission_dao = PermissionDAO(session=self.session)
        permissions: list[PermissionModel] = permission_dao.list(dto=ListPermissionInputDTO(group_id=model.id))
        permission_presenter = ListPermissionPresenter(session=self.session)

        group = Group(
            id=model.id,
            name=model.name,
            permissions=permission_presenter.present(permissions)
        )

        return group
