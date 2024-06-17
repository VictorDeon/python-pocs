from ..dtos import FindUserOutputDTO
from ..interfaces import PresenterInterface


class FindUserPresenter(PresenterInterface):
    """
    Formatação de saída da API que busca um usuário.
    """

    def present(self, output_dto: FindUserOutputDTO) -> dict:
        """
        Forma final de apresentação dos dados.
        """

        return output_dto.user.to_dict()
