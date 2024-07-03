from src.adapters.dtos import RetrievePermissionOutputDTO
from src.adapters import PresenterInterface
from src.infrastructure.databases.models import Permission as PermissionModel
from src.domains.entities import Permission
from .error import ErrorPresenter


class RetrievePermissionPresenter(PresenterInterface):
    """
    Formatação de saída da API que buscar uma permissão.
    """

    async def present(self, model: PermissionModel) -> RetrievePermissionOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        if not model:
            return await ErrorPresenter(session=self.session).present(
                message="Permissão não encontrada.",
            )

        permission = Permission(
            id=model.id,
            name=model.name,
            code=model.code
        )

        return RetrievePermissionOutputDTO(permission=permission)
