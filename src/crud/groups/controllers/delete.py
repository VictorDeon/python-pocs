from fastapi import Path, status
from src.routes import router
from src.engines.databases import DBConnectionHandler
from ..repositories import DeleteGroupDAO


@router.delete(
    "/groups/{group_id}",
    tags=["Banco de Dados"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta um grupo."
)
async def delete_group(group_id: int = Path(..., description="ID do grupo")):
    """
    Deleta um grupo de usuários.
    """

    async with DBConnectionHandler() as session:
        repository = DeleteGroupDAO(session=session)
        return await repository.execute(group_id)
