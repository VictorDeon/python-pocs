from fastapi import Query
from typing import Optional
from src.application.api.routes import router
from src.adapters.controllers import ListUsersController
from src.adapters.dtos import ListUserInputDTO, ListUserOutputDTO


@router.get(
    "/users",
    tags=["Banco de Dados"],
    response_model=ListUserOutputDTO,
    summary="Lista usuários."
)
async def list_user(
    name: Optional[str] = Query(None, description="Filtrar todos os usuário com nome."),
    email: Optional[str] = Query(None, description="Filtrar todos os usuário com um email."),
    group: Optional[int] = Query(None, description="Filtrar todos os usuário de um determinado grupo."),
    work_company_cnpj: Optional[str] = Query(None, description="Listar todos os funcionários de uma empresa."),
    offset: int = Query(0, description="Pular os N primeiros itens da lista."),
    limit: int = Query(25, description="Quantidade limite de itens que irá aparecer na listagem.")):
    """
    Listas os usuários
    """

    controller = ListUsersController(
        input=ListUserInputDTO(
            name=name,
            email=email,
            group=group,
            work_company_cnpj=work_company_cnpj,
            limit=limit,
            offset=offset
        )
    )
    return await controller.execute()
