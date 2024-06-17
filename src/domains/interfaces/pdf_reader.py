# pylint: disable=missing-function-docstring
from abc import ABC, abstractmethod
from domains.models import InvoiceFileResponse


class PDFReaderInterface(ABC):
    """
    Interface para a leitura de PDF.
    """

    @abstractmethod
    async def list_invoices(self, trace_id: str, year: int, month: int) -> InvoiceFileResponse: pass
