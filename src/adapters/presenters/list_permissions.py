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

    def present(
        self,
        models: list[PermissionModel],
        limit: int = None,
        offset: int = None) -> ListPermissionOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        permissions = []
        presenter = RetrievePermissionPresenter(session=self.session)
        for model in models:
            permission = presenter.present(model).permission
            permissions.append(permission)

        paginated_permissions: list[Permission] = paginated(permissions, offset, limit)

        return ListPermissionOutputDTO(
            total=len(paginated_permissions),
            permissions=paginated_permissions
        )
