from uuid import uuid4
from datetime import datetime
from asyncer import asyncify
from src.infrastructure.pdf import GeneratePDF
from src.infrastructure.storage import StorageSingletonInterface
from src.domains.interfaces import PDFGeneratorInterface
from src.domains.entities import Invoice


class PDFGenerator(PDFGeneratorInterface):
    """
    Caso de uso de procura de um usuários.
    """

    def __init__(self, storage_repository: StorageSingletonInterface) -> None:
        """
        Construtor.
        """

        self.storage_repository = storage_repository

    async def create_invoice(self, data: Invoice) -> bytes:
        """
        Endpoint que gera um pdf a partir dos dados inseridos como parâmetro.
        """

        now = datetime.now()
        trace_id = str(uuid4())

        path_splited = "pdfs/invoices".split("/")
        filename = f"{now.year}_{now.month:02}-invoice-{trace_id}.pdf"
        path = "/".join([*path_splited, filename])

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
            filename=path
        )
        pdf = await asyncify(builder.generate_pdf)()

        await self.storage_repository.upload_from_string(
            path=path,
            content=pdf,
            content_type="application/pdf",
            timeout=600
        )

        return pdf
