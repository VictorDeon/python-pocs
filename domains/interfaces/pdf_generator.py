# pylint: disable=missing-function-docstring
from abc import ABC, abstractmethod
from datetime import datetime
from domains.models import Invoice


class PDFGeneratorInterface(ABC):
    """
    Interface para a geração de PDF.
    """

    @abstractmethod
    async def create_invoice(self, data: Invoice): bytes
