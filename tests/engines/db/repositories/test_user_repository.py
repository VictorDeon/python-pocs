from sqlalchemy import text
from faker import Faker
from engines.db import DBConnectionHandler
from engines.db.repositories import UserRepository

faker = Faker()


def test_user_list():
    """
    Testando a pesquisa dos usuários.
    """

    email = faker.email()
    name = faker.name()
    password = faker.password(8)
    repository = UserRepository()

    created_user = repository.create(
        email=email,
        name=name,
        password=password
    )

    users = repository.list(email=created_user.email)

    assert created_user.id == users[0].id
    assert created_user.name == users[0].name
    assert created_user.email == users[0].email

    with DBConnectionHandler() as database:
        database.session.execute(text(f"DELETE FROM users WHERE id={created_user.id}"))
        database.session.commit()


def test_user_retrieve():
    """
    Testando a pesquisa de um usuário.
    """

    email = faker.email()
    name = faker.name()
    password = faker.password(8)
    repository = UserRepository()

    created_user = repository.create(
        email=email,
        name=name,
        password=password
    )

    user = repository.retrieve(_id=created_user.id)

    assert created_user.id == user.id
    assert created_user.name == user.name
    assert created_user.email == user.email

    with DBConnectionHandler() as database:
        database.session.execute(text(f"DELETE FROM users WHERE id={created_user.id}"))
        database.session.commit()


def test_user_create():
    """
    Testando a criação de um usuário.
    """

    email = faker.email()
    name = faker.name()
    password = faker.password(8)
    repository = UserRepository()

    user = repository.create(
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
