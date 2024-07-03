from src.adapters.dtos import ListPermissionOutputDTO
from src.adapters import PresenterInterface
from src.domains.utils.formatters import paginated
from src.domains.entities import Permission
from src.infrastructure.databases.models import Permission as PermissionModel
from .retrieve_permission import RetrievePermissionPresenter


class ListPermissionPresenter(PresenterInterface):
    """
    Formatação de saída da API que lista as permissões.
    """

    async def present(self, models: list[PermissionModel], limit: int = None, offset: int = None) -> ListPermissionOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        permissions: list[Permission] = []
        presenter = RetrievePermissionPresenter(session=self.session)
        for model in models:
            result = await presenter.present(model)
            permissions.append(result.permission)

        paginated_permissions: list[Permission] = paginated(permissions, offset, limit)

        return ListPermissionOutputDTO(
            total=len(permissions),
            permissions=paginated_permissions
        )
