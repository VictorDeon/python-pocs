from src.adapters.dtos import ListPermissionOutputDTO
from src.adapters import PresenterInterface
from src.infrastructure.databases.models import Permission as PermissionModel
from .retrieve_permission import RetrievePermissionPresenter


class ListPermissionPresenter(PresenterInterface):
    """
    Formatação de saída da API que lista as permissões.
    """

    def present(self, models: list[PermissionModel]) -> ListPermissionOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        permissions = []
        presenter = RetrievePermissionPresenter(session=self.session)
        for model in models:
            permission = presenter.present(model).permission
            permissions.append(permission)

        return ListPermissionOutputDTO(permissions=permissions)
