from src.adapters.dtos import CreatePermissionInputDTO, ListPermissionInputDTO
from .permission import PermissionDAO


async def test_create_permission_dao():
    """
    Testa a criação de permissões pelo DAO.
    """

    dto = CreatePermissionInputDTO(
        name="Permissão de criação de permissões",
        code="permission_create"
    )

    dao = PermissionDAO()
    permission = await dao.create(dto=dto)

    assert permission.id is not None
    assert permission.name == dto.name
    assert permission.code == dto.code

    await dao.delete(_id=permission.id)


async def test_list_by_code_permissions_dao():
    """
    Listando as permissões dos usuários pelo código.
    """

    dao = PermissionDAO()

    dto01 = CreatePermissionInputDTO(
        name="Permissão de criação de permissões",
        code="permission_create"
    )
    permission01 = await dao.create(dto=dto01, commit=False, close_session=False)

    dto02 = CreatePermissionInputDTO(
        name="Permissão de atualização de permissões",
        code="permission_update"
    )
    permission02 = await dao.create(dto=dto02, commit=False, close_session=False)

    dto03 = CreatePermissionInputDTO(
        name="Permissão de listagem de permissões",
        code="permission_list"
    )
    permission03 = await dao.create(dto=dto03, commit=True, close_session=False)

    dto = ListPermissionInputDTO(
        code="permission_create"
    )
    permissions = await dao.list(dto=dto, close_session=False)

    assert len(permissions) == 1
    assert permissions[0].id == permission01.id
    assert permissions[0].name == permission01.name
    assert permissions[0].code == permission01.code

    await dao.delete(_id=permission01.id, commit=False, close_session=False)
    await dao.delete(_id=permission02.id, commit=False, close_session=False)
    await dao.delete(_id=permission03.id, commit=True)

async def test_list_by_name_permissions_dao():
    """
    Listando as permissões dos usuários pelo nome.
    """

    dao = PermissionDAO()

    dto01 = CreatePermissionInputDTO(
        name="Permissão para criação de permissões",
        code="permission_create"
    )
    permission01 = await dao.create(dto=dto01, commit=False, close_session=False)

    dto02 = CreatePermissionInputDTO(
        name="Permissão de atualização de permissões",
        code="permission_update"
    )
    permission02 = await dao.create(dto=dto02, commit=False, close_session=False)

    dto03 = CreatePermissionInputDTO(
        name="Permissão para listagem de permissões",
        code="permission_list"
    )
    permission03 = await dao.create(dto=dto03, commit=True, close_session=False)

    dto = ListPermissionInputDTO(
        name="Permissão para"
    )
    permissions = await dao.list(dto=dto, close_session=False)

    assert len(permissions) == 2
    assert permissions[0].id == permission01.id
    assert permissions[0].name == permission01.name
    assert permissions[0].code == permission01.code
    assert permissions[2].id == permission03.id
    assert permissions[2].name == permission03.name
    assert permissions[2].code == permission03.code

    await dao.delete(_id=permission01.id, commit=False, close_session=False)
    await dao.delete(_id=permission02.id, commit=False, close_session=False)
    await dao.delete(_id=permission03.id, commit=True)
