from src.adapters.dtos import ListUserOutputDTO
from src.adapters import PresenterInterface
from src.infrastructure.databases.models import User as UserModel
from .retrieve_user import RetrieveUserPresenter


class ListUserPresenter(PresenterInterface):
    """
    Formatação de saída da API que listar usuários.
    """

    async def present(self, models: list[UserModel]) -> ListUserOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveUserPresenter(session=self.session)
        users: list[UserModel] = []
        for model in models:
            result = await presenter.present(model)
            users.append(result.user)

        return ListUserOutputDTO(users=users)
