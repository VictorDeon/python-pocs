from src.adapters.dtos import CreatePermissionOutputDTO
from src.adapters.interfaces import PresenterInterface
from src.infrastructure.databases.models import Permission as PermissionModel
from src.domains.entities import Permission


class CreatePermissionPresenter(PresenterInterface):
    """
    Formatação de saída da API que cria uma permissão.
    """

    def present(self, permission: PermissionModel) -> CreatePermissionOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        entity = Permission(
            id=permission.id,
            name=permission.name,
            code=permission.code
        )

        return CreatePermissionOutputDTO(permission=entity)
