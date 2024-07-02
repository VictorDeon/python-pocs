from src.adapters.dtos import ListGroupOutputDTO
from src.adapters import PresenterInterface
from src.infrastructure.databases.models import Group as GroupModel
from .retrieve_group import RetrieveGroupPresenter


class ListGroupPresenter(PresenterInterface):
    """
    Formatação de saída da API que listar grupos.
    """

    async def present(self, models: list[GroupModel]) -> ListGroupOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        groups = []
        presenter = RetrieveGroupPresenter(session=self.session)
        for model in models:
            group = await presenter.present(model)
            groups.append(group)

        return ListGroupOutputDTO(groups=groups)
