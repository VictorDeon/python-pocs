from pydantic import BaseModel, Field


class ErrorOutputDTO(BaseModel):
    """
    Dados de saída para erros
    """

    message: str = Field(..., description="Mensagem de error")


class ErrorPresenter:
    """
    Formatação de saída da API que dispara um error.
    """

    async def present(self, message: str) -> ErrorOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        return ErrorOutputDTO(message=message)
