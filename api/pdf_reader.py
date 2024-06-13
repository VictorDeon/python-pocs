from engines.storage import StorageSingleton
from fastapi import Query
from typing import Optional, List
from pydantic import BaseModel, Field
from . import router


class ProductResponse(BaseModel):
    """
    Dados dos produtos da invoice.
    """

    description: str = Field(..., description="Descrição do produto.")
    price: float = Field(..., description="Preço unitário do produto.")
    quantity: int = Field(..., description="Quantidade do produto.")


class InvoiceResponse(BaseModel):
    """
    Dados da invoice.
    """

    from_address: str = Field(..., description="Endereço de destino.")
    to_address: str = Field(..., description="Endereço de origem.")
    invoice_number: str = Field(..., description="Número da invoice.")
    due_date: str = Field(..., description="Data de vencimento da invoice.")
    products: List[ProductResponse] = Field([], description="Lista de produtos da invoice.")
    account: str = Field(..., description="Conta bancária")
    total: float = Field(..., description="Valor total da invoice.")


class InvoiceFileResponse(BaseModel):
    """
    Dados de saída.
    """

    filename: str = Field(..., description="Nome do arquivo no bucket.")
    invoice: InvoiceResponse = Field(None, description="Dados da invoice.")


def handler_path(trace_id: str = None, year: int = None, month: int = None) -> str:
    """
    Cria o caminho de filtro do bucket.
    """

    if trace_id and year and month:
        path = "pdfs/invoices/%d_%02d-invoice-%s.pdf" % trace_id
    elif trace_id and year:
        path = "pdfs/invoices/%d_*-invoice-%s.pdf" % trace_id
    elif trace_id and month:
        path = "pdfs/invoices/*_%02d-invoice-%s.pdf" % trace_id
    elif year and month:
        path = "pdfs/invoices/%d_%02d-*.pdf" % trace_id
    elif trace_id:
        path = "pdfs/invoices/*-invoice-%s.pdf" % trace_id
    elif year:
        path = "pdfs/invoices/%d_*.pdf" % year
    elif month:
        path = "pdfs/invoices/*_%02d-*.pdf" % month
    else:
        path = "pdfs/invoices/*.pdf"

    return path


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
    TODO: Fazer a lógica para extrair os dados do PDF
    """

    bucket = StorageSingleton.get_bucket()
    path = handler_path(trace_id, year, month)
    blobs = list(bucket.list_blobs(match_glob=path))
    response = []
    for blob in blobs:
        blob_path_splited = blob.name.split("/")
        filename = blob_path_splited[-1]
        data = {"filename": filename}
        # Extrair dados do pdf e inserir no response
        response.append(data)

    return response
