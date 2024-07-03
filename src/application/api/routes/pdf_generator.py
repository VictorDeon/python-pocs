from src.application.api.routes import router
from src.adapters.dtos import PDFGeneratorInputDTO, PDFGeneratorOutputDTO
from src.adapters.controllers import PDFGeneratorController


@router.post(
    "/pdfs",
    tags=["Outputs"],
    response_model=PDFGeneratorOutputDTO,
    name="Geração de pdf"
)
async def create_pdf(data: PDFGeneratorInputDTO):
    """
    Endpoint que gera um pdf a partir dos dados inseridos como parâmetro.
    """

    controller = PDFGeneratorController(invoice=data)
    return await controller.execute()
