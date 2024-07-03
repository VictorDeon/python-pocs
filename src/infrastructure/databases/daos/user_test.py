from sqlalchemy import select, Select, or_, insert, Insert, bindparam
from src.adapters.dtos import (
    CreateUserInputDTO, CreatePermissionInputDTO,
    CreateGroupInputDTO, CreateProfileInputDTO,
    CreateCompanyInputDTO, ListUserInputDTO,
    RetrieveUserInputDTO, UpdateUserInputDTO,
    UpdateProfileInputDTO, ListPermissionInputDTO,
    ListGroupInputDTO, ListCompaniesInputDTO
)
from src.infrastructure.databases import DBConnectionHandler
from src.infrastructure.databases.models import User
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

        await permission_dao.create(
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

        assert user.id is not None
        assert user.name == dto.name
        assert user.email == dto.email
        assert user.work_company_cnpj == company.cnpj
        assert len(companies) == 0
        assert profile.user_id == user.id
        assert len(permissions) == 1
        assert len(groups) == 1


async def test_list_users_dao():
    """
    Listando os usuários.
    """

    async with DBConnectionHandler() as session:
        dao = UserDAO(session=session)

        dto01 = CreateUserInputDTO(
            name="Usuário 01",
            email="usuario01@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO()
        )
        user01 = await dao.create(dto=dto01, commit=False)

        dto02 = CreateUserInputDTO(
            name="Usuários 02",
            email="usuario02@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO()
        )
        user02 = await dao.create(dto=dto02, commit=False)

        dto03 = CreateUserInputDTO(
            name="Usuários 03",
            email="usuario03@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO()
        )
        user03 = await dao.create(dto=dto03, commit=True)

        dto = ListUserInputDTO()
        users = await dao.list(dto=dto)

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


async def test_list_by_name_users_dao():
    """
    Listando os usuários pelo nome.
    """

    async with DBConnectionHandler() as session:
        dao = UserDAO(session=session)

        dto01 = CreateUserInputDTO(
            name="Usuário 01",
            email="usuario01@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO()
        )
        await dao.create(dto=dto01, commit=False)

        dto02 = CreateUserInputDTO(
            name="Usuários 02",
            email="usuario02@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO()
        )
        user02 = await dao.create(dto=dto02, commit=False)

        dto03 = CreateUserInputDTO(
            name="Usuários 03",
            email="usuario03@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO()
        )
        user03 = await dao.create(dto=dto03, commit=True)

        dto = ListUserInputDTO(name="Usuários")
        users = await dao.list(dto=dto)

        assert len(users) == 2
        assert users[0].id == user02.id
        assert users[0].name == user02.name
        assert users[0].email == user02.email
        assert users[1].id == user03.id
        assert users[1].name == user03.name
        assert users[1].email == user03.email


async def test_list_by_email_users_dao():
    """
    Listando os usuários pelo email.
    """

    async with DBConnectionHandler() as session:
        dao = UserDAO(session=session)

        dto01 = CreateUserInputDTO(
            name="Usuário 01",
            email="usuario01@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO()
        )
        await dao.create(dto=dto01, commit=False)

        dto02 = CreateUserInputDTO(
            name="Usuários 02",
            email="usuario02@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO()
        )
        user02 = await dao.create(dto=dto02, commit=False)

        dto03 = CreateUserInputDTO(
            name="Usuários 03",
            email="usuario03@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO()
        )
        await dao.create(dto=dto03, commit=True)

        dto = ListUserInputDTO(name="Usuários", email="usuario02@gmail.com")
        users = await dao.list(dto=dto)

        assert len(users) == 1
        assert users[0].id == user02.id
        assert users[0].name == user02.name
        assert users[0].email == user02.email


async def test_list_by_work_company_users_dao():
    """
    Listando os usuários pelo empresa na qual trabalha.
    """

    async with DBConnectionHandler() as session:
        dao = UserDAO(session=session)

        dto01 = CreateUserInputDTO(
            name="Usuário 01",
            email="usuario01@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO()
        )
        await dao.create(dto=dto01, commit=False)

        dto02 = CreateUserInputDTO(
            name="Usuários 02",
            email="usuario02@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO()
        )
        user02 = await dao.create(dto=dto02, commit=False)

        company_dao = CompanyDAO(session=session)
        company = await company_dao.create(
            dto=CreateCompanyInputDTO(
                cnpj="11111111111111",
                name="Empresa 01 LTDA",
                fantasy_name="Empresa 01",
                owner_id=user02.id
            )
        )

        dto03 = CreateUserInputDTO(
            name="Usuários 03",
            email="usuario03@gmail.com",
            password="Django1234",
            work_company_cnpj=company.cnpj,
            profile=CreateProfileInputDTO()
        )
        user03 = await dao.create(dto=dto03, commit=True)

        dto = ListUserInputDTO(work_company_cnpj=company.cnpj)
        users = await dao.list(dto=dto)

        assert len(users) == 1
        assert users[0].id == user03.id
        assert users[0].name == user03.name
        assert users[0].email == user03.email


async def test_list_by_groups_users_dao():
    """
    Listando os usuários pelo email.
    """

    async with DBConnectionHandler() as session:
        user_dao = UserDAO(session=session)
        group_dao = GroupDAO(session=session)

        group_dto01 = CreateGroupInputDTO(name="Grupo01")
        group01 = await group_dao.create(dto=group_dto01, commit=False)

        group_dto02 = CreateGroupInputDTO(name="Grupo02")
        group02 = await group_dao.create(dto=group_dto02, commit=True)

        dto01 = CreateUserInputDTO(
            name="Usuário 01",
            email="usuario01@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO(),
            groups=[group01.id]
        )
        await user_dao.create(dto=dto01, commit=False)

        dto02 = CreateUserInputDTO(
            name="Usuários 02",
            email="usuario02@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO(),
            groups=[group01.id]
        )
        user02 = await user_dao.create(dto=dto02, commit=False)

        dto03 = CreateUserInputDTO(
            name="Usuários 03",
            email="usuario03@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO(),
            groups=[group02.id]
        )
        user03 = await user_dao.create(dto=dto03, commit=True)

        dto = ListUserInputDTO(groups=[group01.id, group02.id], name="Usuários")
        users = await user_dao.list(dto=dto)

        assert len(users) == 2
        assert users[0].id == user02.id
        assert users[0].name == user02.name
        assert users[0].email == user02.email
        assert users[1].id == user03.id
        assert users[1].name == user03.name
        assert users[1].email == user03.email


async def test_get_by_id_user_dao():
    """
    Testa a busca de um usuário pelo identificador.
    """

    async with DBConnectionHandler() as session:
        dao = UserDAO(session=session)

        dto = CreateUserInputDTO(
            name="Usuário 01",
            email="usuario01@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO()
        )
        user = await dao.create(dto=dto, commit=True)

        searched_user = await dao.get_by_id(_id=user.id)

        assert user.id == searched_user.id
        assert user.name == searched_user.name
        assert user.email == searched_user.email


async def test_retrieve_by_email_user_dao():
    """
    Testa a busca de uma permissão pelo código.
    """

    async with DBConnectionHandler() as session:
        dao = UserDAO(session=session)

        dto = CreateUserInputDTO(
            name="Usuário 01",
            email="usuario01@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO()
        )
        user = await dao.create(dto=dto, commit=True)

        dto = RetrieveUserInputDTO(
            email="usuario01@gmail.com"
        )

        searched_user = await dao.retrieve(dto=dto)

        assert user.id == searched_user.id
        assert user.name == searched_user.name
        assert user.email == searched_user.email


async def test_update_user_dao():
    """
    Testa a atualização dos dados do usuário.
    """

    async with DBConnectionHandler() as session:
        dao = UserDAO(session=session)

        permission_dao = PermissionDAO(session=session)
        await permission_dao.create(
            dto=CreatePermissionInputDTO(
                name="Teste permissão para criação de permissões",
                code="t_permission_create"
            )
        )

        await permission_dao.create(
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

        owner_dto = CreateUserInputDTO(
            name="Usuário dono",
            email="usuariodono@gmail.com",
            password="Django1234",
            profile=CreateProfileInputDTO()
        )
        owner = await dao.create(dto=owner_dto, commit=True)

        company_dao = CompanyDAO(session=session)
        company = await company_dao.create(
            dto=CreateCompanyInputDTO(
                cnpj="11111111111111",
                name="Empresa 01 LTDA",
                fantasy_name="Empresa 01",
                owner_id=owner.id
            )
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
        user = await dao.create(dto=dto, commit=True)

        dto = UpdateUserInputDTO(
            name="Usuário 01 Atualizado",
            email="usuario01atualizado@gmail.com",
            profile=UpdateProfileInputDTO(
                phone="6399384945",
                address="Rua sicrano de tal 1111, sorocaba. SP"
            ),
            work_company_cnpj=company.cnpj,
            permissions=["t_permission_update"],
            groups=[]
        )
        updated_user = await dao.update(_id=user.id, dto=dto)
        profile_dao = ProfileDAO(session=session)
        profile = await profile_dao.get_by_id(user_id=updated_user.id)
        permissions = await permission_dao.list(dto=ListPermissionInputDTO(user_id=updated_user.id))
        groups = await group_dao.list(dto=ListGroupInputDTO(user_id=updated_user.id))

        assert user.id == updated_user.id
        assert user.name == updated_user.name
        assert user.email == updated_user.email
        assert updated_user.name == dto.name
        assert updated_user.email == dto.email
        assert profile.phone == dto.profile.phone
        assert profile.address == dto.profile.address
        assert updated_user.work_company_cnpj == dto.work_company_cnpj
        assert len(permissions) == 1
        assert permissions[0].code == "t_permission_update"
        assert len(groups) == 0


async def test_delete_user_dao():
    """
    Testa a deleção do usuário sem deletar os grupos associados e nem
    as permissões, mas deletando o perfil e qualquer empresa vinculada.
    Se for dono da empresa deleta ela, se trabalha na empresa não deleta.
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
            )
        )
        assert group is not None

        user_dao = UserDAO(session=session)
        owner_dto = CreateUserInputDTO(
            name="Fulano dono",
            email="fulanodono@gmail.com",
            password="******",
            profile=CreateProfileInputDTO()
        )
        owner_user = await user_dao.create(dto=owner_dto)
        assert owner_user is not None

        company_dao = CompanyDAO(session=session)
        work_company = await company_dao.create(
            dto=CreateCompanyInputDTO(
                cnpj="11111111111111",
                name="Empresa 01 LTDA",
                fantasy_name="Empresa 01",
                owner_id=owner_user.id
            )
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
        user = await user_dao.create(dto=dto)
        assert user is not None

        company = await company_dao.create(
            dto=CreateCompanyInputDTO(
                cnpj="22222222222222",
                name="Empresa 02 LTDA",
                fantasy_name="Empresa 02",
                owner_id=user.id
            )
        )
        assert company is not None

        await user_dao.delete(_id=user.id)

        company = await company_dao.retrieve(cnpj=company.cnpj)
        assert company is None

        profile_dao = ProfileDAO(session=session)
        profile = await profile_dao.get_by_id(user_id=user.id)
        assert profile is None

        work_company = await company_dao.retrieve(cnpj=work_company.cnpj)
        assert work_company is not None

        owner_user = await user_dao.get_by_id(_id=owner_user.id)
        assert owner_user is not None

        await user_dao.delete(_id=owner_user.id)

        work_company = await company_dao.retrieve(cnpj=work_company.cnpj)
        assert work_company is None

        permission = await permission_dao.get_by_id(_id=permission.id)
        assert permission is not None

        group = await group_dao.get_by_id(_id=group.id)
        assert group is not None

        await group_dao.delete(_id=group.id)
        await permission_dao.delete(_id=permission.id)


async def test_complexy_queries():
    """
    Testando algumas queries complexas.
    stmt = (
        select(func.sum(OrderProducts.quantity).label('quantity'), User.full_name.label('name'))
        .join(Order, Order.order_id == OrderProducts.order_id)
        .join(User)
        .group_by(User.telegram_id)
        .having(func.sum(OrderProducts.quantity) > 10)
    )
    """

    async with DBConnectionHandler() as session:
        users = [
            {
                "name": "Fulano 01",
                "email": "fulano01@gmail.com",
                "password": "Django1234",
            },
            {
                "name": "Fulano 02",
                "email": "fulano02@gmail.com",
                "password": "Django1234",
            },
            {
                "name": "Fulano 03",
                "email": "fulano03@gmail.com",
                "password": "Django1234",
            },
            {
                "name": "Fulano 04",
                "email": "fulano04@gmail.com",
                "password": "Django1234",
            },
            {
                "name": "Fulano 05",
                "email": "fulano05@gmail.com",
                "password": "Django1234",
            },
        ]

        statement: Insert = insert(User).values(
            email=bindparam("email"),
            password=bindparam("password"),
            name=bindparam("name")
        ).returning(User)
        await session.execute(statement, params=users)
        await session.commit()

        statement: Select = select(User) \
            .where(
                or_(
                    User.email == "fulano@gmail.com",
                    User.work_company_cnpj == "11111111111111"
                ),
                User.name.ilike("%fulano%")) \
            .order_by(User.created_at.desc()) \
            .limit(10) \
            .having(User.id >= 1) \
            .group_by(User.id)

        result = await session.scalars(statement)
        users: list[User] = result.all()
        assert len(users) == 0
