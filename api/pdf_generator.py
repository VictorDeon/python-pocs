from google.cloud.storage import Blob, Bucket
from fastapi.responses import Response
from engines.storage import StorageSingleton
from asyncer import asyncify
from datetime import datetime
from pydantic import BaseModel, Field
from engines.pdf import GeneratePDF
from uuid import uuid4
from typing import List
from . import router


class ProductInput(BaseModel):
    """
    Produtos.
    """

    description: str = Field(..., description="Descrição do produto.")
    price: float = Field(..., description="Preço unitário do produto.")
    quantity: int = Field(..., description="Quantidade do produto.")


class InvoiceInput(BaseModel):
    """
    Dados de entrada.
    """

    from_address: str = Field(..., description="Endereço de destino.")
    to_address: str = Field(..., description="Endereço de origem.")
    invoice_number: str = Field(..., description="Número da invoice.")
    products: List[ProductInput] = Field([], description="Lista de produtos da invoice.")
    due_date: str = Field(..., description="Data de vencimento da invoice.")
    account: str = Field(..., description="Conta bancária")


def insert_pdf_into_bucket(pdf: Response, now: datetime, trace_id: str, bucket: Bucket) -> Blob:
    """
    Pega o pdf e insere no bucket.
    """

    path_splited = "pdfs/invoices".split("/")
    filename = f"{now.year}_{now.month:02}-invoice-{trace_id}.pdf"
    path = "/".join([*path_splited, filename])
    blob = Blob(path, bucket)
    blob.upload_from_string(pdf.body, content_type=pdf.media_type, timeout=600)
    return blob


@router.post("/invoice", tags=["PDF"], name="Geração de Invoice")
async def invoice(data: InvoiceInput):
    """
    Endpoint que gera um pdf a partir dos dados inseridos como parâmetro.
    """

    now = datetime.now()
    trace_id = str(uuid4())
    bucket = StorageSingleton.get_bucket()

    builder = GeneratePDF(
        template="invoice.html",
        context={
            "now": now.strftime("%B %d, %Y"),
            "invoice_number": data.invoice_number,
            "from_address": data.from_address,
            "to_address": data.to_address,
            "products": data.products,
            "due_date": datetime.strptime(data.due_date, "%Y-%m-%d").strftime("%B %d, %Y"),
            "account": data.account,
            "total": sum([product.price * product.quantity for product in data.products])
        },
        filename="invoice"
    )
    response = await asyncify(builder.get_response)()

    await asyncify(insert_pdf_into_bucket)(response, now, trace_id, bucket)

    return response
