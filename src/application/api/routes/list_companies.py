from fastapi import Query
from typing import Optional
from src.application.api.routes import router
from src.adapters.controllers import ListCompaniesController
from src.adapters.dtos import ListCompaniesInputDTO, ListCompaniesOutputDTO


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

    controller = ListCompaniesController(
        input=ListCompaniesInputDTO(
            name=name,
            owner_id=owner_id,
            limit=limit,
            offset=offset
        )
    )
    return await controller.execute()
