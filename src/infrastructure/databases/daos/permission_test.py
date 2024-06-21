from src.adapters.dtos import CreatePermissionInputDTO
from .permission import PermissionDAO


async def test_create_permission_dao():
    """
    Testa a criação de permissões pelo DAO.
    """

    dto = CreatePermissionInputDTO(
        name="Permissão de criação de usuários",
        code="user_create"
    )

    dao = PermissionDAO()
    permission = await dao.create(dto=dto)

    assert permission.id is not None
    assert permission.name == dto.name
    assert permission.code == dto.code

    await dao.delete(_id=permission.id)
