from faker import Faker
from src.infrastructure.databases.daos import UserDAO
from src.adapters.dtos import (
    CreateUserInputDTO,
    CreateProfileInputDTO
)


async def test_create_user_dao(faker: Faker):
    """
    Testa a criação de usuário no pelo DAO.
    """

    user_dto = CreateUserInputDTO(
        name=faker.name(),
        email=faker.email(),
        password=faker.password(length=15),
        permissions=[1, 2, 3],
        groups=[1],
        profile=CreateProfileInputDTO(
            address=faker.address()
        )
    )

    dao = UserDAO()
    user = await dao.create(user=user_dto)

    assert user.id is not None
    assert user.email == user_dto.email
    assert user.name == user_dto.name
