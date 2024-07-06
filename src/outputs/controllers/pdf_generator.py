from src.routes import router
from ..dtos import PDFGeneratorInputDTO, PDFGeneratorOutputDTO
from ..repositories import PDFGeneratorRepository


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

    controller = PDFGeneratorRepository(input=data)
    return await controller.execute()
