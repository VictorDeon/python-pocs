import os
import asyncio
from unittest import mock
import pytest
import pytest_asyncio
from pathlib import Path
from pyinstrument import Profiler
from faker import Faker
from datetime import datetime, timedelta
from sqlalchemy import delete, Delete
from src.engines.logger import ProjectLoggerSingleton
from src.engines.databases import DBConnectionHandler, models


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
def auto_profile(request):
    profile_path = Path("assets/profiles").mkdir(exist_ok=True)
    profiler = Profiler()
    profiler.start()

    yield

    profiler.stop()
    profiler.write_html(profile_path + f"{request.node.name}.html")


@pytest_asyncio.fixture(autouse=True, scope="function")
async def clean_db():
    """
    Limpando o banco de dados
    """

    logger = ProjectLoggerSingleton.get_logger()
    logger.info("Iniciando teste")

    yield

    logger.info("Finalizando teste")

    now = datetime.now()
    past = now - timedelta(minutes=5)

    async with DBConnectionHandler() as session:
        statement: Delete = delete(models.UsersVsGroups).where(models.UsersVsGroups.created_at >= past)
        await session.execute(statement)

        statement: Delete = delete(models.UsersVsPermissions).where(models.UsersVsPermissions.created_at >= past)
        await session.execute(statement)

        statement: Delete = delete(models.GroupsVsPermissions).where(models.GroupsVsPermissions.created_at >= past)
        await session.execute(statement)

        statement: Delete = delete(models.User).where(models.User.created_at >= past)
        await session.execute(statement)

        statement: Delete = delete(models.Group).where(models.Group.created_at >= past)
        await session.execute(statement)

        statement: Delete = delete(models.Permission).where(models.Permission.created_at >= past)
        await session.execute(statement)

        await session.commit()
