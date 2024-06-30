import pytest
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from src.adapters.dtos import (
    CreatePermissionInputDTO, ListPermissionInputDTO,
    RetrievePermissionInputDTO, UpdatePermissionInputDTO,
    CreateGroupInputDTO, CreateUserInputDTO, CreateProfileInputDTO
)
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

    dao = PermissionDAO()

    dto01 = CreatePermissionInputDTO(
        name="Test Permissão de criação de permissões",
        code="t_permission_create"
    )
    permission01 = await dao.create(dto=dto01, commit=False, close_session=False)

    dto02 = CreatePermissionInputDTO(
        name="Test Permissão de atualização de permissões",
        code="t_permission_update"
    )
    permission02 = await dao.create(dto=dto02, commit=False, close_session=False)

    dto03 = CreatePermissionInputDTO(
        name="Test Permissão de listagem de permissões",
        code="t_permission_list"
    )
    permission03 = await dao.create(dto=dto03, commit=True, close_session=False)

    dto = ListPermissionInputDTO(
        code="t_permission_create"
    )
    permissions = await dao.list(dto=dto, close_session=False)

    try:
        assert len(permissions) == 1
        assert permissions[0].id == permission01.id
        assert permissions[0].name == permission01.name
        assert permissions[0].code == permission01.code
    finally:
        await dao.delete(_id=permission01.id, commit=False, close_session=False)
        await dao.delete(_id=permission02.id, commit=False, close_session=False)
        await dao.delete(_id=permission03.id, commit=True)


async def test_list_by_name_permissions_dao():
    """
    Listando as permissões dos usuários pelo nome.
    """

    dao = PermissionDAO()

    dto01 = CreatePermissionInputDTO(
        name="Test Permissão para criação de permissões",
        code="t_permission_create"
    )
    permission01 = await dao.create(dto=dto01, commit=False, close_session=False)

    dto02 = CreatePermissionInputDTO(
        name="Test Permissão de atualização de permissões",
        code="t_permission_update"
    )
    permission02 = await dao.create(dto=dto02, commit=False, close_session=False)

    dto03 = CreatePermissionInputDTO(
        name="Test Permissão para listagem de permissões",
        code="t_permission_list"
    )
    permission03 = await dao.create(dto=dto03, commit=True, close_session=False)

    dto = ListPermissionInputDTO(
        name="Test Permissão para"
    )
    permissions = await dao.list(dto=dto, close_session=False)

    try:
        assert len(permissions) == 2
        assert permissions[0].id == permission01.id
        assert permissions[0].name == permission01.name
        assert permissions[0].code == permission01.code
        assert permissions[1].id == permission03.id
        assert permissions[1].name == permission03.name
        assert permissions[1].code == permission03.code
    finally:
        await dao.delete(_id=permission01.id, commit=False, close_session=False)
        await dao.delete(_id=permission02.id, commit=False, close_session=False)
        await dao.delete(_id=permission03.id, commit=True)


async def test_list_by_name_and_code_permissions_dao():
    """
    Listando as permissões dos usuários pelo nome.
    """

    dao = PermissionDAO()

    dto01 = CreatePermissionInputDTO(
        name="Test Permissão para criação de permissões",
        code="t_permission_create"
    )
    permission01 = await dao.create(dto=dto01, commit=False, close_session=False)

    dto02 = CreatePermissionInputDTO(
        name="Test Permissão de atualização de permissões",
        code="t_permission_update"
    )
    permission02 = await dao.create(dto=dto02, commit=False, close_session=False)

    dto03 = CreatePermissionInputDTO(
        name="Test Permissão para listagem de permissões",
        code="t_permission_list"
    )
    permission03 = await dao.create(dto=dto03, commit=True, close_session=False)

    dto = ListPermissionInputDTO(
        name="Test Permissão para",
        code="t_permission_list"
    )
    permissions = await dao.list(dto=dto, close_session=False)

    try:
        assert len(permissions) == 1
        assert permissions[0].id == permission03.id
        assert permissions[0].name == permission03.name
        assert permissions[0].code == permission03.code
    finally:
        await dao.delete(_id=permission01.id, commit=False, close_session=False)
        await dao.delete(_id=permission02.id, commit=False, close_session=False)
        await dao.delete(_id=permission03.id, commit=True)


async def test_list_all_permissions_dao():
    """
    Listando as permissões dos usuários.
    """

    dao = PermissionDAO()

    dto01 = CreatePermissionInputDTO(
        name="Test Permissão para criação de permissões",
        code="t_permission_create"
    )
    permission01 = await dao.create(dto=dto01, commit=False, close_session=False)

    dto02 = CreatePermissionInputDTO(
        name="Test Permissão de atualização de permissões",
        code="t_permission_update"
    )
    permission02 = await dao.create(dto=dto02, commit=False, close_session=False)

    dto03 = CreatePermissionInputDTO(
        name="Test Permissão para listagem de permissões",
        code="t_permission_list"
    )
    permission03 = await dao.create(dto=dto03, commit=True, close_session=False)

    permissions = await dao.list(dto=None, close_session=False)

    qtd = await dao.count(close_session=False)

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
        await dao.delete(_id=permission01.id, commit=False, close_session=False)
        await dao.delete(_id=permission02.id, commit=False, close_session=False)
        await dao.delete(_id=permission03.id, commit=True)


async def test_get_by_id_permission_dao():
    """
    Testa a busca de uma permissão pelo identificador.
    """

    dto = CreatePermissionInputDTO(
        name="Test Permissão de criação de permissões",
        code="t_permission_create"
    )

    dao = PermissionDAO()
    permission = await dao.create(dto=dto, close_session=False)

    searched_permissions = await dao.get_by_id(_id=permission.id, close_session=False)

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

    dao = PermissionDAO()
    searched_permissions = await dao.get_by_id(_id=999)
    assert searched_permissions is None


async def test_retrieve_by_code_permission_dao():
    """
    Testa a busca de uma permissão pelo código.
    """

    dto01 = CreatePermissionInputDTO(
        name="Test Permissão de criação de permissões",
        code="t_permission_create"
    )

    dao = PermissionDAO()
    permission01 = await dao.create(dto=dto01, close_session=False)

    dto = RetrievePermissionInputDTO(
        code="t_permission_create"
    )

    searched_permissions = await dao.retrieve(dto=dto, close_session=False)

    try:
        assert permission01.id == searched_permissions.id
        assert permission01.name == searched_permissions.name
        assert permission01.code == searched_permissions.code
    finally:
        await dao.delete(_id=permission01.id)


async def test_retrieve_multiples_rows_permission_dao():
    """
    Testa a busca de uma permissão pelo código e disparação exceção de
    multiplos retornos.
    """

    dao = PermissionDAO()

    dto01 = CreatePermissionInputDTO(
        name="Test Permissão para criação de permissões",
        code="t_permission_create"
    )
    permission01 = await dao.create(dto=dto01, commit=False, close_session=False)

    dto02 = CreatePermissionInputDTO(
        name="Test Permissão para listagem de permissões",
        code="t_permission_create"
    )
    permission02 = await dao.create(dto=dto02, commit=True, close_session=False)

    dto = RetrievePermissionInputDTO(
        code="t_permission_create"
    )

    try:
        with pytest.raises(MultipleResultsFound) as exc:
            await dao.retrieve(dto=dto, close_session=False)

        assert 'Multiple rows were found when exactly one was required' in str(exc)
    finally:
        await dao.delete(_id=permission01.id)
        await dao.delete(_id=permission02.id)


async def test_retrieve_not_found_permission_dao():
    """
    Testa a busca de uma permissão pelo código e não encontrando
    """

    dao = PermissionDAO()
    dto = RetrievePermissionInputDTO(code="t_permission_create")
    permission = await dao.retrieve(dto=dto, close_session=False)
    assert permission is None


async def test_update_code_permission_dao():
    """
    Testa a atualização do codigo da parmissão.
    """

    dao = PermissionDAO()

    dto01 = CreatePermissionInputDTO(
        name="Test Permissão para criação de permissões",
        code="t_permission_create"
    )
    permission = await dao.create(dto=dto01, close_session=False)

    dto = UpdatePermissionInputDTO(
        name=permission.name,
        code="t_permission_update"
    )

    updated_permission = await dao.update(_id=permission.id, dto=dto, close_session=False)

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

    dao = PermissionDAO()

    dto01 = CreatePermissionInputDTO(
        name="Test Permissão para criação de permissões",
        code="t_permission_create"
    )
    permission = await dao.create(dto=dto01, close_session=False)

    dto = UpdatePermissionInputDTO(
        name="Test Permissão para atualização de permissões",
        code=permission.code
    )

    updated_permission = await dao.update(_id=permission.id, dto=dto, close_session=False)

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

    dao = PermissionDAO()

    dto01 = CreatePermissionInputDTO(
        name="Test Permissão para criação de permissões",
        code="t_permission_create"
    )
    permission = await dao.create(dto=dto01, close_session=False)

    dto = UpdatePermissionInputDTO(
        name="Test Permissão para atualização de permissões",
        code="t_permission_updated"
    )

    updated_permission = await dao.update(_id=permission.id, dto=dto, close_session=False)

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

    dao = PermissionDAO()

    dto = UpdatePermissionInputDTO(
        name="Test Permissão para atualização de permissões",
        code="t_permission_updated"
    )

    with pytest.raises(NoResultFound) as exc:
        await dao.update(_id=999, dto=dto)

    assert "No row was found when one was required" in str(exc)


async def test_delete_permission_dao():
    """
    Testa a deleção da parmissão sem deletar os grupos associados e nem
    os usuários.
    """

    permission_dao = PermissionDAO()

    dto = CreatePermissionInputDTO(
        name="Test Permissão para criação de permissões",
        code="t_permission_create"
    )
    permission = await permission_dao.create(dto=dto, close_session=False)
    assert permission is not None

    group_dao = GroupDAO()
    group = await group_dao.create(
        dto=CreateGroupInputDTO(
            name="Grupo 03",
            permissions=["t_permission_create"]
        ),
        close_session=False
    )
    assert group is not None

    user_dao = UserDAO()
    dto = CreateUserInputDTO(
        name="Fulano de tal",
        email="fulano@gmail.com",
        password="******",
        profile=CreateProfileInputDTO(phone="6399485956"),
        permissions=[permission.code],
        groups=[group.id]
    )
    user = await user_dao.create(dto=dto, close_session=False)
    assert user is not None

    await permission_dao.delete(_id=permission.id, close_session=False)

    permission = await permission_dao.get_by_id(_id=permission.id, close_session=False)
    assert permission is None

    group = await group_dao.get_by_id(_id=group.id, close_session=False)
    assert group is not None

    user = await user_dao.get_by_id(_id=user.id, close_session=False)
    assert user is not None

    await group_dao.delete(_id=group.id)
    await user_dao.delete(_id=user.id)


async def test_delete_not_found_permission_dao():
    """
    Testa a deleção não encontrado.
    """

    dao = PermissionDAO()

    with pytest.raises(ValueError) as exc:
        await dao.delete(_id=999)

    assert "Permissão com o id 999 não encontrado." in str(exc)
