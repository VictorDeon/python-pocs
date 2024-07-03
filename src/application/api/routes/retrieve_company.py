from fastapi import Path
from src.application.api.routes import router
from src.adapters.controllers import GetCompanyByCNPJController
from src.adapters.dtos import RetrieveCompanyOutputDTO


@router.get(
    "/companies/{cnpj}",
    tags=["Banco de Dados"],
    response_model=RetrieveCompanyOutputDTO,
    summary="Busca uma empresa."
)
async def retrieve_company(cnpj: str = Path(..., description="CNPJ da empresa.")):
    """
    Busca uma empresa.
    """

    controller = GetCompanyByCNPJController(cnpj)
    return await controller.execute()
