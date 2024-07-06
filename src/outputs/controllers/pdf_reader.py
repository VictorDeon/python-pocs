from typing import Optional
from fastapi import Query
from src.routes import router
from ..dtos import PDFReaderOutputDTO
from ..repositories import PDFReaderRepository


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

    controller = PDFReaderRepository(trace_id, year, month)
    return await controller.execute()
