from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.formatters import paginated
from ..models import Permission
from .retrieve import RetrievePermissionPresenter
from ..dtos import ListPermissionOutputDTO, RetrievePermissionOutputDTO


class ListPermissionPresenter:
    """
    Formatação de saída da API que lista as permissões.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, models: list[Permission], limit: int = None, offset: int = None) -> ListPermissionOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        permissions: list[RetrievePermissionOutputDTO] = []
        presenter = RetrievePermissionPresenter(session=self.session)
        for model in models:
            permission = await presenter.present(model)
            permissions.append(permission)

        paginated_permissions: list[RetrievePermissionOutputDTO] = paginated(permissions, offset, limit)

        return ListPermissionOutputDTO(
            total=len(permissions),
            permissions=paginated_permissions
        )
