from fastapi import Path
from src.application.api.routes import router
from src.adapters.controllers import UpdateCompanyController
from src.adapters.dtos import UpdateCompanyInputDTO, UpdateCompanyOutputDTO


@router.put(
    "/companies/{cnpj}",
    tags=["Banco de Dados"],
    response_model=UpdateCompanyOutputDTO,
    summary="Atualiza uma empresa."
)
async def update_company(
    data: UpdateCompanyInputDTO,
    cnpj: str = Path(..., description="CNPJ da empresa")):
    """
    Atualiza uma empresa.
    """

    controller = UpdateCompanyController(cnpj, input=data)
    return await controller.execute()
