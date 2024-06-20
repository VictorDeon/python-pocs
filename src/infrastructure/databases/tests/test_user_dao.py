from faker import Faker
from src.infrastructure.databases.daos import UserDAO


async def test_create_user_dao(faker: Faker):
    """
    Testa a criação de usuário no pelo DAO.
    """

    email = faker.email()
    name = faker.name()
    password = faker.password(length=15)
    address = faker.address()

    dao = UserDAO()
    user = await dao.create(
        email=email,
        name=name,
        password=password,
        address=address,
    )

    assert user.id is not None
    assert user.email == email
    assert user.name == name
    assert user.profile.address == address
