from src.adapters.dtos import CreateUserOutputDTO
from src.adapters import PresenterInterface
from src.infrastructure.databases.models import User as UserModel
from .retrieve_user import RetrieveUserPresenter


class CreateUserPresenter(PresenterInterface):
    """
    Formatação de saída da API que cria um usuário.
    """

    async def present(self, model: UserModel) -> CreateUserOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveUserPresenter(session=self.session)
        result = await presenter.present(model)
        return CreateUserOutputDTO(user=result.user)
