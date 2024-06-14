import pytest
from sqlalchemy import text
from faker import Faker
from engines.db import DBConnectionHandler
from adapters import UserRepository

faker = Faker()


def test_user_repository():
    """
    Testando a criação de um usuário.
    """

    email = faker.email()
    name = faker.name()
    password = faker.password(8)

    user = UserRepository.create(
        email=email,
        name=name,
        password=password
    )

    with DBConnectionHandler() as database:
        response = database.session.execute(text(f"SELECT * from users WHERE id={user.id}"))
        result = response.fetchone()

        assert user.id == result.id
        assert user.name == result.name
        assert user.email == result.email

        database.session.execute(text(f"DELETE FROM users WHERE id={user.id}"))
        database.session.commit()
