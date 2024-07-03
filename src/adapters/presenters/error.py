from src.adapters.dtos import ErrorOutputDTO
from src.adapters.presenter_interface import PresenterInterface


class ErrorPresenter(PresenterInterface):
    """
    Formatação de saída da API que dispara um error.
    """

    async def present(self, message: str) -> ErrorOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        return ErrorOutputDTO(message=message)
