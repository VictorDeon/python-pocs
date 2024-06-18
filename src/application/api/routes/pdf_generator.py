from src.adapters.dtos import PDFGeneratorInputDTO, PDFGeneratorOutputDTO
from src.adapters.controllers import PDFGeneratorController
from src.application.api.routes import router


@router.post(
    "/invoices",
    tags=["PDFs"],
    response_model=PDFGeneratorOutputDTO,
    name="Geração de Invoice"
)
async def create_invoice(data: PDFGeneratorInputDTO):
    """
    Endpoint que gera um pdf a partir dos dados inseridos como parâmetro.
    """

    controller = PDFGeneratorController(invoice=data)
    return await controller.execute()
