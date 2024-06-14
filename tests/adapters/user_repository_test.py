from faker import Faker
from adapters import UserRepository

faker = Faker()


def test_user_create():
    """
    Testando a criação do usuário.
    """

    name = faker.name()
    password = faker.word()
    email = faker.email()
    UserRepository.create(name=name, email=email, password=password)
