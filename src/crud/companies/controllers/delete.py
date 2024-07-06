from fastapi import Path, status
from src.routes import router
from src.engines.databases import DBConnectionHandler
from ..repositories import DeleteCompanyDAO


@router.delete(
    "/companies/{cnpj}",
    tags=["CRUDs"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma empresa."
)
async def delete_company(cnpj: str = Path(..., description="CNPJ da empresa")):
    """
    Deleta uma empresa.
    """

    async with DBConnectionHandler() as session:
        repository = DeleteCompanyDAO(session=session)
        return await repository.execute(cnpj)
