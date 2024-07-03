from src.adapters.dtos import CreatePermissionOutputDTO
from src.adapters import PresenterInterface
from src.infrastructure.databases.models import Permission as PermissionModel
from .retrieve_permission import RetrievePermissionPresenter


class CreatePermissionPresenter(PresenterInterface):
    """
    Formatação de saída da API que cria uma permissão.
    """

    async def present(self, model: PermissionModel) -> CreatePermissionOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = await RetrievePermissionPresenter(session=self.session).present(model)
        return CreatePermissionOutputDTO(permission=presenter.permission)
