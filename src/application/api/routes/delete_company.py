from fastapi import Path
from src.application.api.routes import router
from src.adapters.controllers import DeleteCompanyController


@router.delete(
    "/companies/{cnpj}",
    tags=["Banco de Dados"],
    summary="Deleta uma empresa."
)
async def delete_company(cnpj: str = Path(..., description="CNPJ da empresa")):
    """
    Deleta uma empresa.
    """

    controller = DeleteCompanyController(cnpj)
    return await controller.execute()
