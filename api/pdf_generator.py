from asyncer import asyncify
from datetime import datetime
from pydantic import BaseModel, Field
from engines.pdf import GeneratePDF
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


@router.post("/invoice", tags=["PDF"], name="Geração de Invoice")
async def invoice(data: InvoiceInput):
    """
    Endpoint que gera um pdf a partir dos dados inseridos como parâmetro.
    """

    builder = GeneratePDF(
        template="invoice.html",
        context={
            "now": datetime.now().strftime("%B %d, %Y"),
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

    with open("invoice.pdf", "wb") as f:
        f.write(response.body)

    return response