from uuid import uuid4
from datetime import datetime
from asyncer import asyncify
from src.engines.storage import LocalStorageSingleton
from src.engines.pdf import GeneratePDF
from ..dtos import PDFGeneratorInputDTO
from ..presenters import PDFGeneratorPresenter


class PDFGeneratorRepository:
    """
    Controladora de acesso externo para buscar os dados de uma API.
    """

    def __init__(self, input: PDFGeneratorInputDTO) -> None:
        """
        Construtor
        """

        self.input_dto = input

    async def execute(self) -> dict:
        """
        Lida com a entrada e saida dos dados.
        """

        now = datetime.now()
        trace_id = str(uuid4())

        path_splited = "assets/docs".split("/")
        filename = f"{now.year}-{now.month:02}-invoice-{trace_id}.pdf"
        path = "/".join([*path_splited, filename])

        builder = GeneratePDF(
            template="invoice.html",
            context={
                "now": now.strftime("%B %d, %Y"),
                "invoice_number": self.input_dto.invoice_number,
                "from_address": self.input_dto.from_address,
                "to_address": self.input_dto.to_address,
                "products": self.input_dto.products,
                "due_date": datetime.strptime(self.input_dto.due_date, "%Y-%m-%d").strftime("%B %d, %Y"),
                "account": self.input_dto.account,
                "total": sum([product.price * product.quantity for product in self.input_dto.products])
            },
            filename=path
        )
        pdf = await asyncify(builder.generate_pdf)()

        repository = await LocalStorageSingleton.get_instance()
        await repository.upload_from_string(
            path=path,
            content=pdf,
            content_type="application/pdf",
            timeout=600
        )

        return await PDFGeneratorPresenter().present(path)
