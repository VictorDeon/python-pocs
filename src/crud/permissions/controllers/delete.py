from fastapi import Path, status
from src.routes import router
from src.engines.databases import DBConnectionHandler
from ..repositories import DeletePermissionDAO


@router.delete(
    "/permissions/{permission_id}",
    tags=["CRUDs"],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma permissão."
)
async def delete_permission(permission_id: int = Path(..., description="ID da permissão")):
    """
    Deleta uma permissão do usuário ou grupo.
    """

    async with DBConnectionHandler() as session:
        repository = DeletePermissionDAO(session=session)
        await repository.execute(permission_id)
