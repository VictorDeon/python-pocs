from fastapi import Response, status
from src.adapters.interfaces import ControllerInterface
from src.domains.entities import Invoice
from src.domains.interfaces import PDFGeneratorInterface


class PDFGeneratorController(ControllerInterface):
    """
    Controladora de acesso externo para buscar os dados de uma API.
    """

    def __init__(self, user_case: PDFGeneratorInterface) -> None:
        """
        Construtor
        """

        self.__user_case = user_case

    async def execute(self, data: Invoice) -> Response:
        """
        Lida com a entrada e saida dos dados.
        """

        pdf = await self.__user_case.create_invoice(data)

        return Response(
            content=pdf,
            media_type='application/pdf',
            status_code=status.HTTP_201_CREATED
        )
