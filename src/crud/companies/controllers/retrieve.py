from fastapi import Path
from typing import Union
from src.routes import router
from src.engines.databases import DBConnectionHandler
from src.shared.error import ErrorOutputDTO
from ..dtos import RetrieveCompanyOutputDTO
from ..repositories import RetrieveCompanyDAO
from ..presenters import RetrieveCompanyPresenter


@router.get(
    "/companies/{cnpj}",
    tags=["CRUDs"],
    response_model=Union[RetrieveCompanyOutputDTO, ErrorOutputDTO],
    summary="Busca uma empresa."
)
async def retrieve_company(cnpj: str = Path(..., description="CNPJ da empresa.")):
    """
    Busca uma empresa.
    """

    async with DBConnectionHandler() as session:
        repository = RetrieveCompanyDAO(session=session)
        output = RetrieveCompanyPresenter(session=session)
        model = await repository.retrieve(cnpj)
        return await output.present(model)
