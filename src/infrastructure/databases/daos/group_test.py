from src.adapters.dtos import (
    CreateGroupInputDTO, CreatePermissionInputDTO,
    ListGroupInputDTO, UpdateGroupInputDTO
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
            name="Teste permissão para criação de permissões",
            code="t_permission_create"
        ),
        close_session=False
    )

    permission02 = await permission_dao.create(
        dto=CreatePermissionInputDTO(
            name="Teste permissão para atualização de permissões",
            code="t_permission_update"
        ),
        close_session=False
    )

    dao = GroupDAO()
    dto = CreateGroupInputDTO(
        name="Grupo 01",
        permissions=["t_permission_create", "t_permission_update"]
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


async def test_create_not_found_group_dao():
    """
    Testa a criação de grupo pelo DAO com permissão nao encontrada.
    """

    permission_dao = PermissionDAO()
    permission01 = await permission_dao.create(
        dto=CreatePermissionInputDTO(
            name="Teste permissão para criação de permissões",
            code="t_permission_create"
        ),
        close_session=False
    )

    permission02 = await permission_dao.create(
        dto=CreatePermissionInputDTO(
            name="Teste permissão para atualização de permissões",
            code="t_permission_update"
        ),
        close_session=False
    )

    dao = GroupDAO()
    dto = CreateGroupInputDTO(
        name="Grupo 01",
        permissions=["t_permission_create", "t_permission_update_wrong"]
    )

    group = await dao.create(
        dto=dto,
        close_session=False
    )

    try:
        assert group.id is not None
        assert group.name == dto.name
        assert group.permissions.count() == 1
        assert group.permissions[0] == permission01
    finally:
        await dao.delete(_id=group.id)
        await permission_dao.delete(_id=permission01.id)
        await permission_dao.delete(_id=permission02.id)


async def test_list_by_permission_code_group_dao():
    """
    Testa a listagem de grupos pelo código da permissão.
    """

    permission_dao = PermissionDAO()
    permission01 = await permission_dao.create(
        dto=CreatePermissionInputDTO(
            name="Teste permissão para criação de permissões",
            code="t_permission_create"
        ),
        close_session=False
    )

    permission02 = await permission_dao.create(
        dto=CreatePermissionInputDTO(
            name="Teste permissão para atualização de permissões",
            code="t_permission_update"
        ),
        close_session=False
    )

    dao = GroupDAO()
    group01 = await dao.create(
        dto=CreateGroupInputDTO(
            name="Grupo 01",
            permissions=["t_permission_create", "t_permission_update"]
        ),
        close_session=False
    )

    group02 = await dao.create(
        dto=CreateGroupInputDTO(
            name="Grupo 02",
            permissions=["t_permission_update"]
        ),
        close_session=False
    )

    group03 = await dao.create(
        dto=CreateGroupInputDTO(
            name="Grupo 03",
            permissions=[]
        ),
        close_session=False
    )

    dto = ListGroupInputDTO(code="t_permission_update")
    groups = await dao.list(dto=dto, close_session=False)

    try:
        assert len(groups) == 2
        assert groups[0].id == group01.id
        assert groups[0].name == group01.name
        assert groups[0].permissions.count() == 2
        assert groups[1].id == group02.id
        assert groups[1].name == group02.name
        assert groups[1].permissions.count() == 1
    finally:
        await dao.delete(_id=group01.id)
        await dao.delete(_id=group02.id)
        await dao.delete(_id=group03.id)
        await permission_dao.delete(_id=permission01.id)
        await permission_dao.delete(_id=permission02.id)


async def test_list_by_name_group_dao():
    """
    Testa a listagem de grupos pelo nome.
    """

    permission_dao = PermissionDAO()
    permission01 = await permission_dao.create(
        dto=CreatePermissionInputDTO(
            name="Teste permissão para criação de permissões",
            code="t_permission_create"
        ),
        close_session=False
    )

    permission02 = await permission_dao.create(
        dto=CreatePermissionInputDTO(
            name="Teste permissão para atualização de permissões",
            code="t_permission_update"
        ),
        close_session=False
    )

    dao = GroupDAO()
    group01 = await dao.create(
        dto=CreateGroupInputDTO(
            name="Grupo 01",
            permissions=["t_permission_create", "t_permission_update"]
        ),
        close_session=False
    )

    group02 = await dao.create(
        dto=CreateGroupInputDTO(
            name="Grupo 02",
            permissions=["t_permission_update"]
        ),
        close_session=False
    )

    group03 = await dao.create(
        dto=CreateGroupInputDTO(
            name="Grupo 03",
            permissions=[]
        ),
        close_session=False
    )

    dto = ListGroupInputDTO(name="Grupo")
    groups = await dao.list(dto=dto, close_session=False)

    try:
        assert len(groups) == 3
        assert groups[0].id == group01.id
        assert groups[0].name == group01.name
        assert groups[0].permissions.count() == 2
        assert groups[1].id == group02.id
        assert groups[1].name == group02.name
        assert groups[1].permissions.count() == 1
        assert groups[2].id == group03.id
        assert groups[2].name == group03.name
        assert groups[2].permissions.count() == 0
    finally:
        await dao.delete(_id=group01.id)
        await dao.delete(_id=group02.id)
        await dao.delete(_id=group03.id)
        await permission_dao.delete(_id=permission01.id)
        await permission_dao.delete(_id=permission02.id)


async def test_list_by_permission_code_and_group_name_group_dao():
    """
    Testa a listagem de grupos pelo código da permissão e por seu nome.
    """

    permission_dao = PermissionDAO()
    permission01 = await permission_dao.create(
        dto=CreatePermissionInputDTO(
            name="Teste permissão para criação de permissões",
            code="t_permission_create"
        ),
        close_session=False
    )

    permission02 = await permission_dao.create(
        dto=CreatePermissionInputDTO(
            name="Teste permissão para atualização de permissões",
            code="t_permission_update"
        ),
        close_session=False
    )

    dao = GroupDAO()
    group01 = await dao.create(
        dto=CreateGroupInputDTO(
            name="Grupo 01",
            permissions=["t_permission_create", "t_permission_update"]
        ),
        close_session=False
    )

    group02 = await dao.create(
        dto=CreateGroupInputDTO(
            name="Grupo 02",
            permissions=["t_permission_update"]
        ),
        close_session=False
    )

    group03 = await dao.create(
        dto=CreateGroupInputDTO(
            name="Grupo 03",
            permissions=[]
        ),
        close_session=False
    )

    dto = ListGroupInputDTO(name="Grupo", code="t_permission_update")
    groups = await dao.list(dto=dto, close_session=False)

    try:
        assert len(groups) == 2
        assert groups[0].id == group01.id
        assert groups[0].name == group01.name
        assert groups[0].permissions.count() == 2
        assert groups[1].id == group02.id
        assert groups[1].name == group02.name
        assert groups[1].permissions.count() == 1
    finally:
        await dao.delete(_id=group01.id)
        await dao.delete(_id=group02.id)
        await dao.delete(_id=group03.id)
        await permission_dao.delete(_id=permission01.id)
        await permission_dao.delete(_id=permission02.id)


async def test_get_by_id_group_dao():
    """
    Testa a busca de um grupo pelo identificador.
    """

    dao = GroupDAO()
    group = await dao.create(
        dto=CreateGroupInputDTO(
            name="Grupo 03",
            permissions=[]
        ),
        close_session=False
    )

    seached_group = await dao.get_by_id(_id=group.id, close_session=False)

    try:
        assert group.id == seached_group.id
        assert group.name == seached_group.name
        assert group.permissions.count() == 0
    finally:
        await dao.delete(_id=group.id)


async def test_update_group_dao():
    """
    Testa a atualização do grupo.
    """

    permission_dao = PermissionDAO()
    permission = await permission_dao.create(
        dto=CreatePermissionInputDTO(
            name="Teste permissão para criação de permissões",
            code="t_permission_create"
        ),
        close_session=False
    )

    dao = GroupDAO()
    group = await dao.create(
        dto=CreateGroupInputDTO(
            name="Grupo 03",
            permissions=[]
        ),
        close_session=False
    )

    dto = UpdateGroupInputDTO(
        name="Grupo 01",
        permissions=["t_permission_create"]
    )

    updated_group = await dao.update(_id=group.id, dto=dto, close_session=False)

    try:
        assert group.id == updated_group.id
        assert group.name == updated_group.name
        assert updated_group.permissions.count() == 1
    finally:
        await dao.delete(_id=group.id)
        await permission_dao.delete(_id=permission.id)
