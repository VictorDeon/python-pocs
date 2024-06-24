from src.adapters.dtos import (
    CreateUserInputDTO, CreatePermissionInputDTO,
    CreateGroupInputDTO, CreateCompanyInputDTO,
    CreateProfileInputDTO
)
from .group import GroupDAO
from .permission import PermissionDAO
from .user import UserDAO


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

    group_dao = GroupDAO()
    group = await group_dao.create(
        dto=CreateGroupInputDTO(
            name="Grupo 01",
            permissions=["t_permission_create", "t_permission_update"]
        ),
        close_session=False
    )

    user_dao = UserDAO()
    dto = CreateUserInputDTO(
        name="Fulano de tal",
        email="fulano@gmail.com",
        password="******",
        companies=[
            CreateCompanyInputDTO(
                cnpj="11111111111111",
                name="Empresa X LTDA",
                fantasy_name="Empresa X"
            ),
            CreateCompanyInputDTO(
                cnpj="22222222222222",
                name="Empresa Y LTDA",
                fantasy_name="Empresa Y"
            ),
        ],
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
        assert user.companies.count() == 2
        assert user.profile is not None
        assert user.permissions.count() == 1
        assert user.groups.count() == 1
    finally:
        await group_dao.delete(_id=group.id)
        await permission_dao.delete(_id=permission01.id)
        await permission_dao.delete(_id=permission02.id)
