from fastapi import Response
from src.adapters.interfaces import ControllerInterface
from domains.interfaces import PDFReaderInterface
import json


class PDFReaderController(ControllerInterface):
    """
    Controladora de acesso externo para buscar os dados de uma API.
    """

    def __init__(self, user_case: PDFReaderInterface) -> None:
        """
        Construtor
        """

        self.__user_case = user_case

    async def execute(self, trace_id: str, year: int, month: int) -> Response:
        """
        Lida com a entrada e saida dos dados.
        """

        data = await self.__user_case.list_invoices(trace_id, year, month)

        return Response(
            content=json.dumps(data),
            media_type='application/json',
            status_code=200
        )
