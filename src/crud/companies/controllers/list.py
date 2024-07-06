from fastapi import Query
from typing import Optional
from src.routes import router
from src.engines.databases import DBConnectionHandler
from ..dtos import ListCompaniesInputDTO, ListCompaniesOutputDTO
from ..presenters import ListCompanyPresenter
from ..repositories import ListCompanyDAO


@router.get(
    "/companies",
    tags=["Banco de Dados"],
    response_model=ListCompaniesOutputDTO,
    summary="Lista empresas."
)
async def list_companies(
    name: Optional[str] = Query(None, description="Filtra pelo nome da empresa."),
    owner_id: Optional[int] = Query(None, description="Filtra pelo identificador do dona da empresa."),
    offset: int = Query(0, description="Pular os N primeiros itens da lista."),
    limit: int = Query(25, description="Quantidade limite de itens que irá aparecer na listagem.")):
    """
    Listas as empresas.
    """

    async with DBConnectionHandler() as session:
        repository = ListCompanyDAO(session=session)
        output = ListCompanyPresenter(session=session)
        data = ListCompaniesInputDTO(
            name=name,
            owner_id=owner_id,
            limit=limit,
            offset=offset
        )
        models = await repository.list(dto=data)
        return await output.present(models, limit=limit, offset=offset)
