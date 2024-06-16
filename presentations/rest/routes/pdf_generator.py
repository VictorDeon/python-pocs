from domains.models import Invoice
from engines.storage.repositories import LocalStorageSingleton
from domains.user_cases import PDFGenerator
from presentations.rest.controllers import PDFGeneratorController
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

    import pdb
    pdb.set_trace()

    storage = await LocalStorageSingleton.get_instance()
    pdf_generator = PDFGenerator(storage_repository=storage)
    controller = PDFGeneratorController(user_case=pdf_generator)
    await controller.send(data)
    return {"success": True}
