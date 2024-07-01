from src.adapters.dtos import (
    CreateUserInputDTO, CreatePermissionInputDTO,
    CreateGroupInputDTO, CreateProfileInputDTO,
    CreateCompanyInputDTO, ListUserInputDTO,
    RetrieveUserInputDTO, UpdateUserInputDTO,
    UpdateProfileInputDTO, ListPermissionInputDTO,
    ListGroupInputDTO, ListCompaniesInputDTO
)
from src.infrastructure.databases import DBConnectionHandler
from .group import GroupDAO
from .permission import PermissionDAO
from .user import UserDAO
from .company import CompanyDAO
from .profile import ProfileDAO


async def test_create_user_dao():
    """
    Testa a criação de usuários pelo DAO.
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

        group_dao = GroupDAO(session=session)
        group = await group_dao.create(
            dto=CreateGroupInputDTO(
                name="Grupo 01",
                permissions=["t_permission_create", "t_permission_update"]
            )
        )

        user_dao = UserDAO(session=session)
        owner_dto = CreateUserInputDTO(
            name="Usuários dono",
            email="usuario-dono@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO()
        )
        user_owner = await user_dao.create(dto=owner_dto)

        company_dao = CompanyDAO(session=session)
        company = await company_dao.create(
            dto=CreateCompanyInputDTO(
                cnpj="11111111111111",
                name="Empresa 01 LTDA",
                fantasy_name="Empresa 01",
                owner_id=user_owner.id
            )
        )

        dto = CreateUserInputDTO(
            name="Fulano de tal",
            email="fulano@gmail.com",
            password="******",
            work_company_cnpj=company.cnpj,
            profile=CreateProfileInputDTO(phone="6399485956"),
            permissions=[permission01.code],
            groups=[group.id]
        )
        user = await user_dao.create(dto=dto)
        permissions = await permission_dao.list(dto=ListPermissionInputDTO(user_id=user.id))
        groups = await group_dao.list(dto=ListGroupInputDTO(user_id=user.id))
        companies = await company_dao.list(dto=ListCompaniesInputDTO(owner_id=user.id))
        profile_dao = ProfileDAO(session=session)
        profile = await profile_dao.get_by_id(user_id=user.id)

        try:
            assert user.id is not None
            assert user.name == dto.name
            assert user.email == dto.email
            assert user.work_company_cnpj == company.cnpj
            assert len(companies) == 0
            assert profile.user_id == user.id
            assert len(permissions) == 1
            assert len(groups) == 1
        finally:
            await user_dao.delete(_id=user.id)
            await user_dao.delete(_id=user_owner.id)
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
        assert len(users) == await dao.count()
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

    searched_user = await dao.get_by_id(_id=user.id, close_session=False)

    try:
        assert user.id == searched_user.id
        assert user.name == searched_user.name
        assert user.email == searched_user.email
    finally:
        await dao.delete(_id=user.id)


async def test_retrieve_by_email_user_dao():
    """
    Testa a busca de uma permissão pelo código.
    """

    dao = UserDAO()

    dto = CreateUserInputDTO(
        name="Usuário 01",
        email="usuario01@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO()
    )
    user = await dao.create(dto=dto, commit=True, close_session=False)

    dto = RetrieveUserInputDTO(
        email="usuario01@gmail.com"
    )

    searched_user = await dao.retrieve(dto=dto, close_session=False)

    try:
        assert user.id == searched_user.id
        assert user.name == searched_user.name
        assert user.email == searched_user.email
    finally:
        await dao.delete(_id=user.id)


async def test_update_name_user_dao():
    """
    Testa a atualização do nome do usuário.
    """

    dao = UserDAO()

    dto = CreateUserInputDTO(
        name="Usuário 01",
        email="usuario01@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO()
    )
    user = await dao.create(dto=dto, commit=True, close_session=False)

    dto = UpdateUserInputDTO(name="Usuário 01 Atualizado")
    updated_user = await dao.update(_id=user.id, dto=dto, close_session=False)

    try:
        assert user.id == updated_user.id
        assert user.name == updated_user.name
        assert user.email == updated_user.email
        assert updated_user.name == dto.name
    finally:
        await dao.delete(_id=user.id)


async def test_update_email_user_dao():
    """
    Testa a atualização do nome do usuário e email.
    """

    dao = UserDAO()

    dto = CreateUserInputDTO(
        name="Usuário 01",
        email="usuario01@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO()
    )
    user = await dao.create(dto=dto, commit=True, close_session=False)

    dto = UpdateUserInputDTO(
        name="Usuário 01 Atualizado",
        email="usuario01atualizado@gmail.com"
    )
    updated_user = await dao.update(_id=user.id, dto=dto, close_session=False)

    try:
        assert user.id == updated_user.id
        assert user.name == updated_user.name
        assert user.email == updated_user.email
        assert updated_user.name == dto.name
        assert updated_user.email == dto.email
    finally:
        await dao.delete(_id=user.id)


async def test_update_profile_user_dao():
    """
    Testa a atualização do nome do usuário e email e dados do perfil.
    """

    dao = UserDAO()

    dto = CreateUserInputDTO(
        name="Usuário 01",
        email="usuario01@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO(
            phone="11111111111",
            address="Rua fulano de tal 2039, sorocaba. SP"
        )
    )
    user = await dao.create(dto=dto, commit=True, close_session=False)

    dto = UpdateUserInputDTO(
        name="Usuário 01 Atualizado",
        email="usuario01atualizado@gmail.com",
        profile=UpdateProfileInputDTO(
            phone="6399384945",
            address="Rua sicrano de tal 1111, sorocaba. SP"
        )
    )
    updated_user = await dao.update(_id=user.id, dto=dto, close_session=False)

    try:
        assert user.id == updated_user.id
        assert user.name == updated_user.name
        assert user.email == updated_user.email
        assert updated_user.name == dto.name
        assert updated_user.email == dto.email
        assert updated_user.profile.phone == dto.profile.phone
        assert updated_user.profile.address == dto.profile.address
    finally:
        await dao.delete(_id=user.id)


async def test_update_permissions_user_dao():
    """
    Testa a atualização do nome do usuário e email e dados do perfil
    e permissões.
    """

    dao = UserDAO()

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

    dto = CreateUserInputDTO(
        name="Usuário 01",
        email="usuario01@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO(
            phone="11111111111",
            address="Rua fulano de tal 2039, sorocaba. SP"
        ),
        permissions=["t_permission_create"]
    )
    user = await dao.create(dto=dto, commit=True, close_session=False)

    dto = UpdateUserInputDTO(
        name="Usuário 01 Atualizado",
        email="usuario01atualizado@gmail.com",
        profile=UpdateProfileInputDTO(
            phone="6399384945",
            address="Rua sicrano de tal 1111, sorocaba. SP"
        ),
        permissions=["t_permission_update"]
    )
    updated_user = await dao.update(_id=user.id, dto=dto, close_session=False)

    try:
        assert user.id == updated_user.id
        assert user.name == updated_user.name
        assert user.email == updated_user.email
        assert updated_user.name == dto.name
        assert updated_user.email == dto.email
        assert updated_user.profile.phone == dto.profile.phone
        assert updated_user.profile.address == dto.profile.address
        assert updated_user.permissions.count() == 1
        assert updated_user.permissions[0].code == "t_permission_update"
    finally:
        await dao.delete(_id=user.id)
        await permission_dao.delete(_id=permission01.id)
        await permission_dao.delete(_id=permission02.id)


async def test_update_groups_user_dao():
    """
    Testa a atualização do nome do usuário e email e dados do perfil
    permissões e grupos.
    """

    dao = UserDAO()

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

    dto = CreateUserInputDTO(
        name="Usuário 01",
        email="usuario01@gmail.com",
        password="Django1234",
        profile=CreateProfileInputDTO(
            phone="11111111111",
            address="Rua fulano de tal 2039, sorocaba. SP"
        ),
        permissions=["t_permission_create"],
        groups=[group.id]
    )
    user = await dao.create(dto=dto, commit=True, close_session=False)

    dto = UpdateUserInputDTO(
        name="Usuário 01 Atualizado",
        email="usuario01atualizado@gmail.com",
        profile=UpdateProfileInputDTO(
            phone="6399384945",
            address="Rua sicrano de tal 1111, sorocaba. SP"
        ),
        permissions=["t_permission_update"],
        groups=[]
    )
    updated_user = await dao.update(_id=user.id, dto=dto, close_session=False)

    try:
        assert user.id == updated_user.id
        assert user.name == updated_user.name
        assert user.email == updated_user.email
        assert updated_user.name == dto.name
        assert updated_user.email == dto.email
        assert updated_user.profile.phone == dto.profile.phone
        assert updated_user.profile.address == dto.profile.address
        assert updated_user.permissions.count() == 1
        assert updated_user.permissions[0].code == "t_permission_update"
        assert updated_user.groups.count() == 0
    finally:
        await dao.delete(_id=user.id)
        await permission_dao.delete(_id=permission01.id)
        await permission_dao.delete(_id=permission02.id)
        await group_dao.delete(_id=group.id)


async def test_delete_user_dao():
    """
    Testa a deleção do usuário sem deletar os grupos associados e nem
    as permissões, mas deletando o perfil e qualquer empresa vinculada.
    Se for dono da empresa deleta ela, se trabalha na empresa não deleta.
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
    owner_dto = CreateUserInputDTO(
        name="Fulano dono",
        email="fulanodono@gmail.com",
        password="******",
        profile=CreateProfileInputDTO()
    )
    owner_user = await user_dao.create(dto=owner_dto, close_session=False)
    assert owner_user is not None

    company_dao = CompanyDAO()
    work_company = await company_dao.create(
        dto=CreateCompanyInputDTO(
            cnpj="11111111111111",
            name="Empresa 01 LTDA",
            fantasy_name="Empresa 01",
            owner_id=owner_user.id
        ),
        close_session=False
    )
    assert work_company is not None

    dto = CreateUserInputDTO(
        name="Fulano de tal",
        email="fulano@gmail.com",
        password="******",
        work_company_cnpj=work_company.cnpj,
        profile=CreateProfileInputDTO(phone="6399485956"),
        permissions=[permission.code],
        groups=[group.id]
    )
    user = await user_dao.create(dto=dto, close_session=False)
    assert user is not None

    company = await company_dao.create(
        dto=CreateCompanyInputDTO(
            cnpj="22222222222222",
            name="Empresa 02 LTDA",
            fantasy_name="Empresa 02",
            owner_id=user.id
        ),
        close_session=False
    )
    assert company is not None

    await user_dao.delete(_id=user.id, close_session=False)

    company = await company_dao.get_by_cnpj(cnpj=company.cnpj, close_session=False)
    assert company is None

    profile_dao = ProfileDAO()
    profile = await profile_dao.get_by_id(_id=user.profile.id, close_session=False)
    assert profile is None

    work_company = await company_dao.get_by_cnpj(cnpj=work_company.cnpj, close_session=False)
    assert work_company is not None

    owner_user = await user_dao.get_by_id(_id=owner_user.id, close_session=False)
    assert owner_user is not None

    await user_dao.delete(_id=owner_user.id, close_session=False)

    work_company = await company_dao.get_by_cnpj(cnpj=work_company.cnpj, close_session=False)
    assert work_company is None

    permission = await permission_dao.get_by_id(_id=permission.id, close_session=False)
    assert permission is not None

    group = await group_dao.get_by_id(_id=group.id, close_session=False)
    assert group is not None

    await permission_dao.delete(_id=permission.id)
    await group_dao.delete(_id=group.id)
