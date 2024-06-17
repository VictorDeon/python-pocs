from src.domains.entities import Invoice
from src.infrastructure.storage.repositories import LocalStorageSingleton
from domains.user_cases import PDFGenerator
from src.adapters.controllers import PDFGeneratorController
from . import router


@router.post(
    "/invoices",
    tags=["PDFs"],
    name="Geração de Invoice"
)
async def create_invoice(data: Invoice):
    """
    Endpoint que gera um pdf a partir dos dados inseridos como parâmetro.
    """

    storage = await LocalStorageSingleton.get_instance()
    pdf_generator = PDFGenerator(storage_repository=storage)
    controller = PDFGeneratorController(user_case=pdf_generator)
    await controller.send(data)
    return {"success": True}
