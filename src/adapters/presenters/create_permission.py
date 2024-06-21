from src.adapters.dtos import CreatePermissionOutputDTO
from src.adapters import PresenterInterface
from src.infrastructure.databases.models import Permission as PermissionModel
from src.domains.entities import Permission


class CreatePermissionPresenter(PresenterInterface):
    """
    Formatação de saída da API que cria uma permissão.
    """

    def present(self, model: PermissionModel) -> CreatePermissionOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        permission = Permission(
            id=model.id,
            name=model.name,
            code=model.code
        )

        return CreatePermissionOutputDTO(permission=permission)
