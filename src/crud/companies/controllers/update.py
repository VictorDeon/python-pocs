from fastapi import Path
from src.routes import router
from src.engines.databases import DBConnectionHandler
from ..dtos import UpdateCompanyInputDTO, UpdateCompanyOutputDTO
from ..repositories import UpdateCompanyDAO
from ..presenters import UpdateCompanyPresenter


@router.put(
    "/companies/{cnpj}",
    tags=["CRUDs"],
    response_model=UpdateCompanyOutputDTO,
    summary="Atualiza uma empresa."
)
async def update_company(
    data: UpdateCompanyInputDTO,
    cnpj: str = Path(..., description="CNPJ da empresa")):
    """
    Atualiza uma empresa.
    """

    async with DBConnectionHandler() as session:
        repository = UpdateCompanyDAO(session=session)
        output = UpdateCompanyPresenter(session=session)
        model = await repository.execute(cnpj, dto=data)
        return await output.present(model)
