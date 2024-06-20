from src.adapters.dtos import CreatePermissionInputDTO
from src.infrastructure.databases.daos import PermissionDAO


async def test_create_permission_dao():
    """
    Testa a criação de permissões pelo DAO.
    """

    dto01 = CreatePermissionInputDTO(
        name = "Permissão de criação de usuários",
        code = "user_create"
    )

    dto02 = CreatePermissionInputDTO(
        name = "Permissão de atualização de usuários",
        code = "user_update"
    )

    dto03 = CreatePermissionInputDTO(
        name = "Permissão de deleção de usuários",
        code = "user_delete"
    )

    dao = PermissionDAO()
    permission01 = await dao.create(dto=dto01)
    permission02 = await dao.create(dto=dto02)
    permission03 = await dao.create(dto=dto03)

    assert permission01.id is not None
    assert permission01.name == dto01.name
    assert permission01.code == dto01.code

    assert permission02.id is not None
    assert permission02.name == dto02.name
    assert permission02.code == dto02.code

    assert permission03.id is not None
    assert permission03.name == dto03.name
    assert permission03.code == dto03.code

