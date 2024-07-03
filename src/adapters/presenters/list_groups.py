from src.adapters.dtos import ListGroupOutputDTO
from src.adapters import PresenterInterface
from src.domains.utils.formatters import paginated
from src.domains.entities import Group
from src.infrastructure.databases.models import Group as GroupModel
from .retrieve_group import RetrieveGroupPresenter


class ListGroupPresenter(PresenterInterface):
    """
    Formatação de saída da API que listar grupos.
    """

    async def present(self, models: list[GroupModel], limit: int = None, offset: int = None) -> ListGroupOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        groups: list[Group] = []
        presenter = RetrieveGroupPresenter(session=self.session)
        for model in models:
            result = await presenter.present(model)
            groups.append(result.group)

        paginated_groups: list[Group] = paginated(groups, offset, limit)

        return ListGroupOutputDTO(
            total=len(groups),
            groups=paginated_groups
        )
