import os
import asyncio
from unittest import mock
import pytest
from faker import Faker


@pytest.fixture(scope="session")
def event_loop():
    """
    Abre e fecha loop de corotines após todos os testes
    serem executados.
    """

    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def faker():
    """
    Instancia o faker.
    """

    yield Faker()


@pytest.fixture(autouse=True, scope="session")
def envs():
    """
    Mockando as variaveis de ambiente do projeto.
    """

    with mock.patch.dict(os.environ, {
        "APP_ENV": "tests",
        "GOOGLE_CLOUD_PROJECT": "vksoftware"
    }):
        yield


@pytest.fixture(scope="function")
def db():
    """
    Fixture to populate db and remove after test execution.
    """

    yield


