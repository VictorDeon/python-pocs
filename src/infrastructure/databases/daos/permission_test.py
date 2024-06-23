from src.adapters.dtos import (
    CreatePermissionInputDTO, ListPermissionInputDTO,
    RetrievePermissionInputDTO
)
from sqlalchemy.orm.exc import MultipleResultsFound
from .permission import PermissionDAO
import pytest


async def test_create_permission_dao():
    """
    Testa a criação de permissões pelo DAO.
    """

    dto = CreatePermissionInputDTO(
        name="Permissão de criação de permissões",
        code="permission_create"
    )

    dao = PermissionDAO()
    permission = await dao.create(dto=dto, close_session=False)

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
    assert permissions[1].id == permission03.id
    assert permissions[1].name == permission03.name
    assert permissions[1].code == permission03.code

    await dao.delete(_id=permission01.id, commit=False, close_session=False)
    await dao.delete(_id=permission02.id, commit=False, close_session=False)
    await dao.delete(_id=permission03.id, commit=True)

async def test_list_by_name_and_code_permissions_dao():
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
        name="Permissão para",
        code="permission_list"
    )
    permissions = await dao.list(dto=dto, close_session=False)

    assert len(permissions) == 1
    assert permissions[0].id == permission03.id
    assert permissions[0].name == permission03.name
    assert permissions[0].code == permission03.code

    await dao.delete(_id=permission01.id, commit=False, close_session=False)
    await dao.delete(_id=permission02.id, commit=False, close_session=False)
    await dao.delete(_id=permission03.id, commit=True)

async def test_get_by_id_permission_dao():
    """
    Testa a busca de uma permissão pelo identificador.
    """

    dto = CreatePermissionInputDTO(
        name="Permissão de criação de permissões",
        code="permission_create"
    )

    dao = PermissionDAO()
    permission = await dao.create(dto=dto, close_session=False)

    searched_permissions = await dao.get_by_id(_id=permission.id, close_session=False)

    assert permission.id == searched_permissions.id
    assert permission.name == searched_permissions.name
    assert permission.code == searched_permissions.code

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
        name="Permissão de criação de permissões",
        code="permission_create"
    )

    dao = PermissionDAO()
    permission01 = await dao.create(dto=dto01, close_session=False)

    dto = RetrievePermissionInputDTO(
        code="permission_create"
    )

    searched_permissions = await dao.retrieve(dto=dto, close_session=False)

    assert permission01.id == searched_permissions.id
    assert permission01.name == searched_permissions.name
    assert permission01.code == searched_permissions.code

    await dao.delete(_id=permission01.id)


async def test_retrieve_multiples_rows_permission_dao():
    """
    Testa a busca de uma permissão pelo código e disparação exceção de
    multiplos retornos.
    """

    dao = PermissionDAO()

    dto01 = CreatePermissionInputDTO(
        name="Permissão para criação de permissões",
        code="permission_create"
    )
    permission01 = await dao.create(dto=dto01, commit=False, close_session=False)

    dto02 = CreatePermissionInputDTO(
        name="Permissão para listagem de permissões",
        code="permission_create"
    )
    permission02 = await dao.create(dto=dto02, commit=True, close_session=False)

    dto = RetrievePermissionInputDTO(
        code="permission_create"
    )

    with pytest.raises(MultipleResultsFound) as exc:
        await dao.retrieve(dto=dto, close_session=False)

    assert 'Multiple rows were found when exactly one was required' in str(exc)

    await dao.delete(_id=permission01.id)
    await dao.delete(_id=permission02.id)


async def test_retrieve_not_found_permission_dao():
    """
    Testa a busca de uma permissão pelo código e disparação exceção de
    multiplos retornos.
    """

    dao = PermissionDAO()
    dto = RetrievePermissionInputDTO(code="permission_create")
    permission = await dao.retrieve(dto=dto, close_session=False)
    assert permission is None

