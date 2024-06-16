from fastapi import Response, status
from presentations.rest.controller import ControllerInterface
from domains.models import Invoice
from domains.interfaces import PDFGeneratorInterface


class PDFGeneratorController(ControllerInterface):
    """
    Controladora de acesso externo para buscar os dados de uma API.
    """

    def __init__(self, user_case: PDFGeneratorInterface) -> None:
        """
        Construtor
        """

        self.__user_case = user_case

    async def send(self, data: Invoice) -> Response:
        """
        Lida com a entrada e saida dos dados.
        """

        pdf = await self.__user_case.create_invoice(data)

        return Response(
            content=pdf,
            media_type='application/pdf',
            status_code=status.HTTP_201_CREATED
        )
