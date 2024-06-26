from src.adapters.dtos import (
    CreateUserInputDTO, CreatePermissionInputDTO,
    CreateGroupInputDTO, CreateProfileInputDTO,
    CreateCompanyInputDTO, ListUserInputDTO
)
from .group import GroupDAO
from .permission import PermissionDAO
from .user import UserDAO
from .company import CompanyDAO


async def test_create_user_dao():
    """
    Testa a criação de usuários pelo DAO.
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

    group_dao = GroupDAO()
    group = await group_dao.create(
        dto=CreateGroupInputDTO(
            name="Grupo 01",
            permissions=["t_permission_create", "t_permission_update"]
        ),
        close_session=False
    )

    company_dao = CompanyDAO()
    company = await company_dao.create(
        dto=CreateCompanyInputDTO(
            cnpj="11111111111111",
            name="Empresa 01 LTDA",
            fantasy_name="Empresa 01"
        ),
        close_session=False
    )

    user_dao = UserDAO()
    dto = CreateUserInputDTO(
        name="Fulano de tal",
        email="fulano@gmail.com",
        password="******",
        work_company_cnpj=company.cnpj,
        profile=CreateProfileInputDTO(phone="6399485956"),
        permissions=[permission01.code],
        groups=[group.id]
    )
    user = await user_dao.create(
        dto=dto,
        close_session=False
    )

    try:
        assert user.id is not None
        assert user.name == dto.name
        assert user.email == dto.email
        assert user.work_company_cnpj == company.cnpj
        assert user.work_company == company
        assert len(user.companies) == 0
        assert user.profile is not None
        assert user.permissions.count() == 1
        assert user.groups.count() == 1
    finally:
        await user_dao.delete(_id=user.id)
        await company_dao.delete(cnpj=company.cnpj)
        await group_dao.delete(_id=group.id)
        await permission_dao.delete(_id=permission01.id)
        await permission_dao.delete(_id=permission02.id)


async def test_list_users_dao():
    """
    Listando os usuários.
    """

    dao = UserDAO()

    dto01 = CreateUserInputDTO(
        name="Usuário 01",
        email="usuario01@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO()
    )
    user01 = await dao.create(dto=dto01, commit=False, close_session=False)

    dto02 = CreateUserInputDTO(
        name="Usuários 02",
        email="usuario02@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO()
    )
    user02 = await dao.create(dto=dto02, commit=False, close_session=False)

    dto03 = CreateUserInputDTO(
        name="Usuários 03",
        email="usuario03@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO()
    )
    user03 = await dao.create(dto=dto03, commit=True, close_session=False)

    dto = ListUserInputDTO()
    users = await dao.list(dto=dto, close_session=False)

    try:
        assert len(users) == 3
        assert users[0].id == user01.id
        assert users[0].name == user01.name
        assert users[0].email == user01.email
        assert users[1].id == user02.id
        assert users[1].name == user02.name
        assert users[1].email == user02.email
        assert users[2].id == user03.id
        assert users[2].name == user03.name
        assert users[2].email == user03.email
    finally:
        await dao.delete(_id=user01.id, commit=False, close_session=False)
        await dao.delete(_id=user02.id, commit=False, close_session=False)
        await dao.delete(_id=user03.id, commit=True)


async def test_list_by_name_users_dao():
    """
    Listando os usuários pelo nome.
    """

    dao = UserDAO()

    dto01 = CreateUserInputDTO(
        name="Usuário 01",
        email="usuario01@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO()
    )
    user01 = await dao.create(dto=dto01, commit=False, close_session=False)

    dto02 = CreateUserInputDTO(
        name="Usuários 02",
        email="usuario02@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO()
    )
    user02 = await dao.create(dto=dto02, commit=False, close_session=False)

    dto03 = CreateUserInputDTO(
        name="Usuários 03",
        email="usuario03@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO()
    )
    user03 = await dao.create(dto=dto03, commit=True, close_session=False)

    dto = ListUserInputDTO(name="Usuários")
    users = await dao.list(dto=dto, close_session=False)

    try:
        assert len(users) == 2
        assert users[0].id == user02.id
        assert users[0].name == user02.name
        assert users[0].email == user02.email
        assert users[1].id == user03.id
        assert users[1].name == user03.name
        assert users[1].email == user03.email
    finally:
        await dao.delete(_id=user01.id, commit=False, close_session=False)
        await dao.delete(_id=user02.id, commit=False, close_session=False)
        await dao.delete(_id=user03.id, commit=True)


async def test_list_by_email_users_dao():
    """
    Listando os usuários pelo email.
    """

    dao = UserDAO()

    dto01 = CreateUserInputDTO(
        name="Usuário 01",
        email="usuario01@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO()
    )
    user01 = await dao.create(dto=dto01, commit=False, close_session=False)

    dto02 = CreateUserInputDTO(
        name="Usuários 02",
        email="usuario02@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO()
    )
    user02 = await dao.create(dto=dto02, commit=False, close_session=False)

    dto03 = CreateUserInputDTO(
        name="Usuários 03",
        email="usuario03@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO()
    )
    user03 = await dao.create(dto=dto03, commit=True, close_session=False)

    dto = ListUserInputDTO(name="Usuários", email="usuario02@gmail.com")
    users = await dao.list(dto=dto, close_session=False)

    try:
        assert len(users) == 1
        assert users[0].id == user02.id
        assert users[0].name == user02.name
        assert users[0].email == user02.email
    finally:
        await dao.delete(_id=user01.id, commit=False, close_session=False)
        await dao.delete(_id=user02.id, commit=False, close_session=False)
        await dao.delete(_id=user03.id, commit=True)


async def test_list_by_groups_users_dao():
    """
    Listando os usuários pelo email.
    """

    user_dao = UserDAO()
    group_dao = GroupDAO()

    group_dto01 = CreateGroupInputDTO(name="Grupo01")
    group01 = await group_dao.create(dto=group_dto01, commit=False, close_session=False)

    group_dto02 = CreateGroupInputDTO(name="Grupo02")
    group02 = await group_dao.create(dto=group_dto02, commit=True, close_session=False)

    dto01 = CreateUserInputDTO(
        name="Usuário 01",
        email="usuario01@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO(),
        groups=[group01.id]
    )
    user01 = await user_dao.create(dto=dto01, commit=False, close_session=False)

    dto02 = CreateUserInputDTO(
        name="Usuários 02",
        email="usuario02@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO(),
        groups=[group01.id]
    )
    user02 = await user_dao.create(dto=dto02, commit=False, close_session=False)

    dto03 = CreateUserInputDTO(
        name="Usuários 03",
        email="usuario03@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO(),
        groups=[group02.id]
    )
    user03 = await user_dao.create(dto=dto03, commit=True, close_session=False)

    dto = ListUserInputDTO(groups=["Grupo 01", "Grupo 02"])
    users = await user_dao.list(dto=dto, close_session=False)

    try:
        assert len(users) == 3
        assert users[0].id == user01.id
        assert users[0].name == user01.name
        assert users[0].email == user01.email
        assert users[1].id == user02.id
        assert users[1].name == user02.name
        assert users[1].email == user02.email
        assert users[2].id == user03.id
        assert users[2].name == user03.name
        assert users[2].email == user03.email
    finally:
        await group_dao.delete(_id=group01.id, commit=False, close_session=False)
        await group_dao.delete(_id=group02.id, commit=False, close_session=False)
        await user_dao.delete(_id=user01.id, commit=False, close_session=False)
        await user_dao.delete(_id=user02.id, commit=False, close_session=False)
        await user_dao.delete(_id=user03.id, commit=True)


async def test_get_by_id_user_dao():
    """
    Testa a busca de um usuário pelo identificador.
    """

    dao = UserDAO()

    dto = CreateUserInputDTO(
        name="Usuário 01",
        email="usuario01@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO()
    )
    user = await dao.create(dto=dto, commit=True, close_session=False)

    searched_permissions = await dao.get_by_id(_id=user.id, close_session=False)

    try:
        assert user.id == searched_permissions.id
        assert user.name == searched_permissions.name
        assert user.email == searched_permissions.email
    finally:
        await dao.delete(_id=user.id)
