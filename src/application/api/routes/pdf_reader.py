from typing import Optional, List
from fastapi import Query
from src.adapters.dtos import PDFReaderOutputDTO
from src.adapters.controllers import PDFReaderController
from src.application.api.routes import router


@router.get(
    "/invoices",
    tags=["PDFs"],
    name="Lista de Invoices",
    response_model=PDFReaderOutputDTO
)
async def list_invoices(
    trace_id: Optional[str] = Query(None, title="Trace ID", description="Identificador único da invoice"),
    year: Optional[int] = Query(None, title="Ano", description="Ano na qual a invoice foi criada."),
    month: Optional[int] = Query(None, title="Mês", description="Mês na qual a invoice foi criada.")):
    """
    Endpoint que lista todos os pdfs inserido no bucket e puxa seus dados retornando em json.
    """

    controller = PDFReaderController(trace_id, year, month)
    return await controller.execute()
