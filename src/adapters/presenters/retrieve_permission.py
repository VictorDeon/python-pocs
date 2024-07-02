from src.adapters.dtos import RetrievePermissionOutputDTO
from src.adapters import PresenterInterface
from src.infrastructure.databases.models import Permission as PermissionModel
from src.domains.entities import Permission


class RetrievePermissionPresenter(PresenterInterface):
    """
    Formatação de saída da API que buscar uma permissão.
    """

    def present(self, model: PermissionModel) -> RetrievePermissionOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        permission = Permission(
            id=model.id,
            name=model.name,
            code=model.code
        )

        return RetrievePermissionOutputDTO(permission=permission)
