from typing import Optional
from fastapi import Query
from src.application.api.routes import router
from src.adapters.dtos import PDFReaderOutputDTO
from src.adapters.controllers import PDFReaderController


@router.get(
    "/pdfs",
    tags=["Outputs"],
    name="Lista de PDFs",
    response_model=PDFReaderOutputDTO
)
async def pdf_reader(
    trace_id: Optional[str] = Query(None, title="Trace ID", description="Identificador único da invoice"),
    year: Optional[int] = Query(None, title="Ano", description="Ano na qual a invoice foi criada."),
    month: Optional[int] = Query(None, title="Mês", description="Mês na qual a invoice foi criada.")):
    """
    Endpoint que lista todos os pdfs inserido no bucket e puxa seus dados retornando em json.
    """

    controller = PDFReaderController(trace_id, year, month)
    return await controller.execute()
