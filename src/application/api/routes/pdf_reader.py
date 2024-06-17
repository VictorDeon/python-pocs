from typing import Optional, List
from fastapi import Query
from domains.models import InvoiceFileResponse
from engines.storage.repositories import LocalStorageSingleton
from domains.user_cases import PDFReader
from src.adapters.controllers import PDFReaderController
from . import router


@router.get(
    "/invoices",
    tags=["PDFs"],
    name="Lista de Invoices",
    response_model=List[InvoiceFileResponse]
)
async def list_invoices(
    trace_id: Optional[str] = Query(None, title="Trace ID", description="Identificador único da invoice"),
    year: Optional[int] = Query(None, title="Ano", description="Ano na qual a invoice foi criada."),
    month: Optional[int] = Query(None, title="Mês", description="Mês na qual a invoice foi criada.")):
    """
    Endpoint que lista todos os pdfs inserido no bucket e puxa seus dados retornando em json.
    """

    storage = await LocalStorageSingleton.get_instance()
    user_case = PDFReader(storage_repository=storage)
    controller = PDFReaderController(user_case=user_case)
    response = await controller.send(trace_id, year, month)
    return response
