import pytest
from src.adapters.dtos import (
    CreatePermissionInputDTO, ListPermissionInputDTO,
    RetrievePermissionInputDTO, UpdatePermissionInputDTO,
    CreateGroupInputDTO, CreateUserInputDTO, CreateProfileInputDTO
)
from src.domains.utils.exceptions import GenericException
from src.infrastructure.databases import DBConnectionHandler
from .permission import PermissionDAO
from .group import GroupDAO
from .user import UserDAO


async def test_create_permission_dao():
    """
    Testa a criação de permissões pelo DAO.
    """

    async with DBConnectionHandler() as session:
        dto = CreatePermissionInputDTO(
            name="Test Permissão de criação de permissões",
            code="t_permission_create"
        )

        dao = PermissionDAO(session=session)
        permission = await dao.create(dto=dto)

        try:
            assert permission.id is not None
            assert permission.name == dto.name
            assert permission.code == dto.code
        finally:
            await dao.delete(_id=permission.id)


async def test_list_by_code_permissions_dao():
    """
    Listando as permissões dos usuários pelo código.
    """

    async with DBConnectionHandler() as session:
        dao = PermissionDAO(session=session)

        dto01 = CreatePermissionInputDTO(
            name="Test Permissão de criação de permissões",
            code="t_permission_create"
        )
        permission01 = await dao.create(dto=dto01, commit=False)

        dto02 = CreatePermissionInputDTO(
            name="Test Permissão de atualização de permissões",
            code="t_permission_update"
        )
        permission02 = await dao.create(dto=dto02, commit=False)

        dto03 = CreatePermissionInputDTO(
            name="Test Permissão de listagem de permissões",
            code="t_permission_list"
        )
        permission03 = await dao.create(dto=dto03, commit=True)

        dto = ListPermissionInputDTO(
            code="t_permission_create"
        )
        permissions = await dao.list(dto=dto)

        try:
            assert len(permissions) == 1
            assert permissions[0].id == permission01.id
            assert permissions[0].name == permission01.name
            assert permissions[0].code == permission01.code
        finally:
            await dao.delete(_id=permission01.id, commit=False)
            await dao.delete(_id=permission02.id, commit=False)
            await dao.delete(_id=permission03.id, commit=True)


async def test_list_by_name_permissions_dao():
    """
    Listando as permissões dos usuários pelo nome.
    """

    async with DBConnectionHandler() as session:
        dao = PermissionDAO(session=session)

        dto01 = CreatePermissionInputDTO(
            name="Test Permissão para criação de permissões",
            code="t_permission_create"
        )
        permission01 = await dao.create(dto=dto01, commit=False)

        dto02 = CreatePermissionInputDTO(
            name="Test Permissão de atualização de permissões",
            code="t_permission_update"
        )
        permission02 = await dao.create(dto=dto02, commit=False)

        dto03 = CreatePermissionInputDTO(
            name="Test Permissão para listagem de permissões",
            code="t_permission_list"
        )
        permission03 = await dao.create(dto=dto03, commit=True)

        dto = ListPermissionInputDTO(
            name="Test Permissão para"
        )
        permissions = await dao.list(dto=dto)

        try:
            assert len(permissions) == 2
            assert permissions[0].id == permission01.id
            assert permissions[0].name == permission01.name
            assert permissions[0].code == permission01.code
            assert permissions[1].id == permission03.id
            assert permissions[1].name == permission03.name
            assert permissions[1].code == permission03.code
        finally:
            await dao.delete(_id=permission01.id, commit=False)
            await dao.delete(_id=permission02.id, commit=False)
            await dao.delete(_id=permission03.id, commit=True)


async def test_list_by_name_and_code_permissions_dao():
    """
    Listando as permissões dos usuários pelo nome.
    """

    async with DBConnectionHandler() as session:
        dao = PermissionDAO(session=session)

        dto01 = CreatePermissionInputDTO(
            name="Test Permissão para criação de permissões",
            code="t_permission_create"
        )
        permission01 = await dao.create(dto=dto01, commit=False)

        dto02 = CreatePermissionInputDTO(
            name="Test Permissão de atualização de permissões",
            code="t_permission_update"
        )
        permission02 = await dao.create(dto=dto02, commit=False)

        dto03 = CreatePermissionInputDTO(
            name="Test Permissão para listagem de permissões",
            code="t_permission_list"
        )
        permission03 = await dao.create(dto=dto03, commit=True)

        dto = ListPermissionInputDTO(
            name="Test Permissão para",
            code="t_permission_list"
        )
        permissions = await dao.list(dto=dto)

        try:
            assert len(permissions) == 1
            assert permissions[0].id == permission03.id
            assert permissions[0].name == permission03.name
            assert permissions[0].code == permission03.code
        finally:
            await dao.delete(_id=permission01.id, commit=False)
            await dao.delete(_id=permission02.id, commit=False)
            await dao.delete(_id=permission03.id, commit=True)


async def test_list_all_permissions_dao():
    """
    Listando as permissões dos usuários.
    """

    async with DBConnectionHandler() as session:
        dao = PermissionDAO(session=session)

        dto01 = CreatePermissionInputDTO(
            name="Test Permissão para criação de permissões",
            code="t_permission_create"
        )
        permission01 = await dao.create(dto=dto01, commit=False)

        dto02 = CreatePermissionInputDTO(
            name="Test Permissão de atualização de permissões",
            code="t_permission_update"
        )
        permission02 = await dao.create(dto=dto02, commit=False)

        dto03 = CreatePermissionInputDTO(
            name="Test Permissão para listagem de permissões",
            code="t_permission_list"
        )
        permission03 = await dao.create(dto=dto03, commit=True)

        permissions = await dao.list(dto=ListPermissionInputDTO())

        qtd = await dao.count()

        try:
            assert len(permissions) == qtd
            assert permissions[0].id == permission01.id
            assert permissions[0].name == permission01.name
            assert permissions[0].code == permission01.code
            assert permissions[1].id == permission02.id
            assert permissions[1].name == permission02.name
            assert permissions[1].code == permission02.code
            assert permissions[2].id == permission03.id
            assert permissions[2].name == permission03.name
            assert permissions[2].code == permission03.code
        finally:
            await dao.delete(_id=permission01.id, commit=False)
            await dao.delete(_id=permission02.id, commit=False)
            await dao.delete(_id=permission03.id, commit=True)


async def test_get_by_id_permission_dao():
    """
    Testa a busca de uma permissão pelo identificador.
    """

    async with DBConnectionHandler() as session:
        dto = CreatePermissionInputDTO(
            name="Test Permissão de criação de permissões",
            code="t_permission_create"
        )

        dao = PermissionDAO(session=session)
        permission = await dao.create(dto=dto)

        searched_permissions = await dao.get_by_id(_id=permission.id)

        try:
            assert permission.id == searched_permissions.id
            assert permission.name == searched_permissions.name
            assert permission.code == searched_permissions.code
        finally:
            await dao.delete(_id=permission.id)


async def test_get_by_id_not_found_permission_dao():
    """
    Testa a busca de uma permissão pelo identificador não encontrado.
    """

    async with DBConnectionHandler() as session:
        dao = PermissionDAO(session=session)
        searched_permissions = await dao.get_by_id(_id=999)
        assert searched_permissions is None


async def test_retrieve_by_code_permission_dao():
    """
    Testa a busca de uma permissão pelo código.
    """

    async with DBConnectionHandler() as session:
        dto01 = CreatePermissionInputDTO(
            name="Test Permissão de criação de permissões",
            code="t_permission_create"
        )

        dao = PermissionDAO(session=session)
        permission01 = await dao.create(dto=dto01)

        dto = RetrievePermissionInputDTO(
            code="t_permission_create"
        )

        searched_permissions = await dao.retrieve(dto=dto)

        try:
            assert permission01.id == searched_permissions.id
            assert permission01.name == searched_permissions.name
            assert permission01.code == searched_permissions.code
        finally:
            await dao.delete(_id=permission01.id)


async def test_retrieve_not_found_permission_dao():
    """
    Testa a busca de uma permissão pelo código e não encontrando
    """

    async with DBConnectionHandler() as session:
        dao = PermissionDAO(session=session)
        dto = RetrievePermissionInputDTO(code="t_permission_create")
        permission = await dao.retrieve(dto=dto)
        assert permission is None


async def test_update_code_permission_dao():
    """
    Testa a atualização do codigo da parmissão.
    """

    async with DBConnectionHandler() as session:
        dao = PermissionDAO(session=session)

        dto01 = CreatePermissionInputDTO(
            name="Test Permissão para criação de permissões",
            code="t_permission_create"
        )
        permission = await dao.create(dto=dto01)

        dto = UpdatePermissionInputDTO(
            name=permission.name,
            code="t_permission_update"
        )

        updated_permission = await dao.update(_id=permission.id, dto=dto)

        try:
            assert permission.id == updated_permission.id
            assert permission.name == updated_permission.name
            assert permission.code == updated_permission.code
            assert updated_permission.code == dto.code
        finally:
            await dao.delete(_id=permission.id)


async def test_update_name_permission_dao():
    """
    Testa a atualização do nome da parmissão.
    """

    async with DBConnectionHandler() as session:
        dao = PermissionDAO(session=session)

        dto01 = CreatePermissionInputDTO(
            name="Test Permissão para criação de permissões",
            code="t_permission_create"
        )
        permission = await dao.create(dto=dto01)

        dto = UpdatePermissionInputDTO(
            name="Test Permissão para atualização de permissões",
            code=permission.code
        )

        updated_permission = await dao.update(_id=permission.id, dto=dto)

        try:
            assert permission.id == updated_permission.id
            assert permission.name == updated_permission.name
            assert permission.code == updated_permission.code
            assert updated_permission.name == dto.name
        finally:
            await dao.delete(_id=permission.id)


async def test_update_all_permission_dao():
    """
    Testa a atualização dos dados da parmissão.
    """

    async with DBConnectionHandler() as session:
        dao = PermissionDAO(session=session)

        dto01 = CreatePermissionInputDTO(
            name="Test Permissão para criação de permissões",
            code="t_permission_create"
        )
        permission = await dao.create(dto=dto01)

        dto = UpdatePermissionInputDTO(
            name="Test Permissão para atualização de permissões",
            code="t_permission_updated"
        )

        updated_permission = await dao.update(_id=permission.id, dto=dto)

        try:
            assert permission.id == updated_permission.id
            assert permission.name == updated_permission.name
            assert permission.code == updated_permission.code
            assert updated_permission.name == dto.name
            assert updated_permission.code == dto.code
        finally:
            await dao.delete(_id=permission.id)


async def test_update_not_found_permission_dao():
    """
    Testa a atualização não encontrado.
    """

    async with DBConnectionHandler() as session:
        dao = PermissionDAO(session=session)

        dto = UpdatePermissionInputDTO(
            name="Test Permissão para atualização de permissões",
            code="t_permission_updated"
        )

        with pytest.raises(GenericException) as exc:
            await dao.update(_id=999, dto=dto)

        assert "Permissão com id 999 não encontrado." in str(exc)


async def test_delete_permission_dao():
    """
    Testa a deleção da parmissão sem deletar os grupos associados e nem
    os usuários.
    """

    async with DBConnectionHandler() as session:
        permission_dao = PermissionDAO(session=session)

        dto = CreatePermissionInputDTO(
            name="Test Permissão para criação de permissões",
            code="t_permission_create"
        )
        permission = await permission_dao.create(dto=dto)
        assert permission is not None

        group_dao = GroupDAO(session=session)
        group = await group_dao.create(
            dto=CreateGroupInputDTO(
                name="Grupo 03",
                permissions=["t_permission_create"]
            ),
            close_session=False
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

        await permission_dao.delete(_id=permission.id)

        permission = await permission_dao.get_by_id(_id=permission.id)
        assert permission is None

        group = await group_dao.get_by_id(_id=group.id)
        assert group is not None

        user = await user_dao.get_by_id(_id=user.id)
        assert user is not None

        await group_dao.delete(_id=group.id)
        await user_dao.delete(_id=user.id)


async def test_delete_not_found_permission_dao():
    """
    Testa a deleção não encontrado.
    """

    async with DBConnectionHandler() as session:
        dao = PermissionDAO(session=session)

        with pytest.raises(GenericException) as exc:
            await dao.delete(_id=999)

        assert "Permissão com id 999 não encontrado." in str(exc)
