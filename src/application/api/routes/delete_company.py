from fastapi import Path, status
from src.application.api.routes import router
from src.adapters.controllers import DeleteCompanyController


@router.delete(
    "/companies/{cnpj}",
    tags=["Banco de Dados"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma empresa."
)
async def delete_company(cnpj: str = Path(..., description="CNPJ da empresa")):
    """
    Deleta uma empresa.
    """

    controller = DeleteCompanyController(cnpj)
    await controller.execute()
