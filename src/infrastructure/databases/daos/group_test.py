from src.adapters.dtos import (
    CreateGroupInputDTO, CreatePermissionInputDTO
)
from .group import GroupDAO
from .permission import PermissionDAO


async def test_create_group_dao():
    """
    Testa a criação de grupo pelo DAO.
    """

    permission_dao = PermissionDAO()
    permission01 = await permission_dao.create(
        dto=CreatePermissionInputDTO(
            name="Permissão para criação de permissões",
            code="permission_create"
        ),
        close_session=False
    )

    permission02 = await permission_dao.create(
        dto=CreatePermissionInputDTO(
            name="Permissão para atualização de permissões",
            code="permission_update"
        ),
        close_session=False
    )

    dao = GroupDAO()
    dto = CreateGroupInputDTO(
        name="Grupo 01",
        permissions=["permission_create", "permission_update"]
    )

    group = await dao.create(
        dto=dto,
        close_session=False
    )

    try:
        assert group.id is not None
        assert group.name == dto.name
        assert group.permissions.count() == 2
        assert group.permissions[0] == permission01
        assert group.permissions[1] == permission02
    finally:
        await dao.delete(_id=group.id)
        await permission_dao.delete(_id=permission01.id)
        await permission_dao.delete(_id=permission02.id)
