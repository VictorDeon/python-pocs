from src.adapters.dtos import UpdatePermissionOutputDTO
from src.adapters import PresenterInterface
from src.infrastructure.databases.models import Permission as PermissionModel
from .retrieve_permission import RetrievePermissionPresenter


class UpdatePermissionPresenter(PresenterInterface):
    """
    Formatação de saída da API que atualizar uma permissão.
    """

    def present(self, model: PermissionModel) -> UpdatePermissionOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrievePermissionPresenter(session=self.session).present(model)
        return UpdatePermissionOutputDTO(permission=presenter.permission)
