from src.adapters.dtos import (
    CreateGroupInputDTO, CreatePermissionInputDTO,
    ListGroupInputDTO, UpdateGroupInputDTO,
    CreateUserInputDTO, CreateProfileInputDTO,
    ListPermissionInputDTO
)
from src.infrastructure.databases import DBConnectionHandler
from .group import GroupDAO
from .permission import PermissionDAO
from .user import UserDAO


async def test_create_group_dao():
    """
    Testa a criação de grupo pelo DAO.
    """

    async with DBConnectionHandler() as session:
        permission_dao = PermissionDAO(session=session)
        permission01 = await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para criação de permissões",
                code="t_permission_create"
            )
        )

        permission02 = await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para atualização de permissões",
                code="t_permission_update"
            )
        )

        dao = GroupDAO(session=session)
        dto = CreateGroupInputDTO(
            name="Grupo 01",
            permissions=["t_permission_create", "t_permission_update"]
        )

        group = await dao.create(dto=dto)
        permissions = await permission_dao.list(dto=ListPermissionInputDTO(group_id=group.id))

        try:
            assert group.id is not None
            assert group.name == dto.name
            assert len(permissions) == 2
            assert permissions[0] == permission01
            assert permissions[1] == permission02
        finally:
            await dao.delete(_id=group.id)
            await permission_dao.delete(_id=permission01.id)
            await permission_dao.delete(_id=permission02.id)


async def test_create_not_found_group_dao():
    """
    Testa a criação de grupo pelo DAO com permissão nao encontrada.
    """

    async with DBConnectionHandler() as session:
        permission_dao = PermissionDAO(session=session)
        permission01 = await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para criação de permissões",
                code="t_permission_create"
            )
        )

        permission02 = await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para atualização de permissões",
                code="t_permission_update"
            )
        )

        dao = GroupDAO(session=session)
        dto = CreateGroupInputDTO(
            name="Grupo 01",
            permissions=["t_permission_create", "t_permission_update_wrong"]
        )

        group = await dao.create(dto=dto)
        permissions = await permission_dao.list(dto=ListPermissionInputDTO(group_id=group.id))

        try:
            assert group.id is not None
            assert group.name == dto.name
            assert len(permissions) == 1
            assert permissions[0] == permission01
        finally:
            await dao.delete(_id=group.id)
            await permission_dao.delete(_id=permission01.id)
            await permission_dao.delete(_id=permission02.id)


async def test_list_by_permission_code_group_dao():
    """
    Testa a listagem de grupos pelo código da permissão.
    """

    async with DBConnectionHandler() as session:
        permission_dao = PermissionDAO(session=session)
        permission01 = await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para criação de permissões",
                code="t_permission_create"
            )
        )

        permission02 = await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para atualização de permissões",
                code="t_permission_update"
            )
        )

        dao = GroupDAO(session=session)
        group01 = await dao.create(
            dto=CreateGroupInputDTO(
                name="Grupo 01",
                permissions=["t_permission_create", "t_permission_update"]
            )
        )

        group02 = await dao.create(
            dto=CreateGroupInputDTO(
                name="Grupo 02",
                permissions=["t_permission_update"]
            )
        )

        group03 = await dao.create(
            dto=CreateGroupInputDTO(
                name="Grupo 03",
                permissions=[]
            )
        )

        dto = ListGroupInputDTO(code="t_permission_update")
        groups = await dao.list(dto=dto)

        try:
            assert len(groups) == 2
            assert groups[0].id == group01.id
            assert groups[0].name == group01.name
            permissions = await permission_dao.list(dto=ListPermissionInputDTO(group_id=groups[0].id))
            assert len(permissions) == 2
            assert groups[1].id == group02.id
            assert groups[1].name == group02.name
            permissions = await permission_dao.list(dto=ListPermissionInputDTO(group_id=groups[1].id))
            assert len(permissions) == 1
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

    async with DBConnectionHandler() as session:
        permission_dao = PermissionDAO(session=session)
        permission01 = await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para criação de permissões",
                code="t_permission_create"
            )
        )

        permission02 = await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para atualização de permissões",
                code="t_permission_update"
            )
        )

        dao = GroupDAO(session=session)
        group01 = await dao.create(
            dto=CreateGroupInputDTO(
                name="Grupo 01",
                permissions=["t_permission_create", "t_permission_update"]
            )
        )

        group02 = await dao.create(
            dto=CreateGroupInputDTO(
                name="Grupo 02",
                permissions=["t_permission_update"]
            )
        )

        group03 = await dao.create(
            dto=CreateGroupInputDTO(
                name="Grupo 03",
                permissions=[]
            )
        )

        dto = ListGroupInputDTO(name="Grupo")
        groups = await dao.list(dto=dto)

        try:
            assert len(groups) == 3
            assert groups[0].id == group01.id
            assert groups[0].name == group01.name
            permissions = await permission_dao.list(dto=ListPermissionInputDTO(group_id=groups[0].id))
            assert len(permissions) == 2
            assert groups[1].id == group02.id
            assert groups[1].name == group02.name
            permissions = await permission_dao.list(dto=ListPermissionInputDTO(group_id=groups[1].id))
            assert len(permissions) == 1
            assert groups[2].id == group03.id
            assert groups[2].name == group03.name
            permissions = await permission_dao.list(dto=ListPermissionInputDTO(group_id=groups[2].id))
            assert len(permissions) == 0
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

    async with DBConnectionHandler() as session:
        permission_dao = PermissionDAO(session=session)
        permission01 = await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para criação de permissões",
                code="t_permission_create"
            )
        )

        permission02 = await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para atualização de permissões",
                code="t_permission_update"
            )
        )

        dao = GroupDAO(session=session)
        group01 = await dao.create(
            dto=CreateGroupInputDTO(
                name="Grupo 01",
                permissions=["t_permission_create", "t_permission_update"]
            )
        )

        group02 = await dao.create(
            dto=CreateGroupInputDTO(
                name="Grupo 02",
                permissions=["t_permission_update"]
            )
        )

        group03 = await dao.create(
            dto=CreateGroupInputDTO(
                name="Grupo 03",
                permissions=[]
            )
        )

        dto = ListGroupInputDTO(name="Grupo", code="t_permission_update")
        groups = await dao.list(dto=dto)

        try:
            assert len(groups) == 2
            assert groups[0].id == group01.id
            assert groups[0].name == group01.name
            permissions = await permission_dao.list(dto=ListPermissionInputDTO(group_id=groups[0].id))
            assert len(permissions) == 2
            assert groups[1].id == group02.id
            assert groups[1].name == group02.name
            permissions = await permission_dao.list(dto=ListPermissionInputDTO(group_id=groups[1].id))
            assert len(permissions) == 1
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

    async with DBConnectionHandler() as session:
        dao = GroupDAO(session=session)
        group = await dao.create(
            dto=CreateGroupInputDTO(
                name="Grupo 03",
                permissions=[]
            )
        )

        seached_group = await dao.get_by_id(_id=group.id)
        permission_dao = PermissionDAO(session=session)
        permissions = await permission_dao.list(dto=ListPermissionInputDTO(group_id=seached_group.id))

        try:
            assert group.id == seached_group.id
            assert group.name == seached_group.name
            assert len(permissions) == 0
        finally:
            await dao.delete(_id=group.id)


async def test_update_group_dao():
    """
    Testa a atualização do grupo.
    """

    async with DBConnectionHandler() as session:
        permission_dao = PermissionDAO(session=session)
        permission01 = await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para criação de permissões",
                code="t_permission_create"
            )
        )
        permission02 = await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para atualização de permissões",
                code="t_permission_update"
            )
        )
        permission03 = await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para deleção de permissões",
                code="t_permission_delete"
            )
        )

        dao = GroupDAO(session=session)
        group = await dao.create(
            dto=CreateGroupInputDTO(
                name="Grupo 03",
                permissions=["t_permission_update"]
            )
        )

        dto = UpdateGroupInputDTO(
            name="Grupo 01",
            permissions=["t_permission_create", "t_permission_delete"]
        )

        try:
            updated_group = await dao.update(_id=group.id, dto=dto)
            permissions = await permission_dao.list(dto=ListPermissionInputDTO(group_id=updated_group.id))

            assert group.id == updated_group.id
            assert updated_group.name == dto.name
            assert len(permissions) == 2
        finally:
            await dao.delete(_id=group.id)
            await permission_dao.delete(_id=permission01.id)
            await permission_dao.delete(_id=permission02.id)
            await permission_dao.delete(_id=permission03.id)


async def test_update_group_permission_clean_dao():
    """
    Testa a atualização do grupo removendo permissões.
    """

    async with DBConnectionHandler() as session:
        permission_dao = PermissionDAO(session=session)
        permission = await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para criação de permissões",
                code="t_permission_create"
            )
        )

        dao = GroupDAO(session=session)
        group = await dao.create(
            dto=CreateGroupInputDTO(
                name="Grupo 03",
                permissions=["t_permission_create"]
            )
        )

        dto = UpdateGroupInputDTO(name="Grupo 03", permissions=[])

        try:
            updated_group = await dao.update(_id=group.id, dto=dto)
            permissions = await permission_dao.list(dto=ListPermissionInputDTO(group_id=updated_group.id))

            assert group.id == updated_group.id
            assert group.name == updated_group.name
            assert len(permissions) == 0
        finally:
            await dao.delete(_id=group.id)
            await permission_dao.delete(_id=permission.id)


async def test_delete_group_dao():
    """
    Testa a deleção da grupo sem deletar as permissões associadas a ele
    e nem os usuários associados a ele.
    """

    async with DBConnectionHandler() as session:
        permission_dao = PermissionDAO(session=session)
        permission = await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para criação de permissões",
                code="t_permission_create"
            )
        )
        assert permission is not None

        group_dao = GroupDAO(session=session)
        group = await group_dao.create(
            dto=CreateGroupInputDTO(
                name="Grupo 03",
                permissions=["t_permission_create"]
            )
        )
        assert group is not None

        user_dao = UserDAO(session=session)
        dto = CreateUserInputDTO(
            name="Fulano de tal",
            email="fulano@gmail.com",
            password="******",
            profile=CreateProfileInputDTO(phone="6399485956"),
            permissions=[permission.code],
            groups=[group.id]
        )
        user = await user_dao.create(dto=dto)
        assert user is not None

        await group_dao.delete(_id=group.id)

        group = await group_dao.get_by_id(_id=group.id)
        assert group is None

        permission = await permission_dao.get_by_id(_id=permission.id)
        assert permission is not None

        user = await user_dao.get_by_id(_id=user.id)
        assert user is not None

        await permission_dao.delete(_id=permission.id)
        await user_dao.delete(_id=user.id)
