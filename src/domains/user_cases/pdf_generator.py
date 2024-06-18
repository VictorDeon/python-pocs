from uuid import uuid4
from datetime import datetime
from asyncer import asyncify
from src.adapters.interfaces import PresenterInterface
from src.adapters.dtos import PDFGeneratorInputDTO
from src.domains.interfaces import UserCaseInterface
from src.infrastructure.pdf import GeneratePDF
from src.infrastructure.storage import StorageSingletonInterface


class PDFGenerator(UserCaseInterface):
    """
    Caso de uso de procura de um usuários.
    """

    def __init__(self, presenter: PresenterInterface, repository: StorageSingletonInterface):
        """
        Constructor.
        """

        self.presenter = presenter
        self.repository = repository

    async def execute(self, input_dto: PDFGeneratorInputDTO) -> dict:
        """
        Endpoint que gera um pdf a partir dos dados inseridos como parâmetro.
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
                "invoice_number": input_dto.invoice_number,
                "from_address": input_dto.from_address,
                "to_address": input_dto.to_address,
                "products": input_dto.products,
                "due_date": datetime.strptime(input_dto.due_date, "%Y-%m-%d").strftime("%B %d, %Y"),
                "account": input_dto.account,
                "total": sum([product.price * product.quantity for product in input_dto.products])
            },
            filename=path
        )
        pdf = await asyncify(builder.generate_pdf)()

        await self.repository.upload_from_string(
            path=path,
            content=pdf,
            content_type="application/pdf",
            timeout=600
        )

        return self.presenter.present(path)
