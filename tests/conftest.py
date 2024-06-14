import pytest
from datetime import datetime, timedelta
from sqlalchemy import text
from engines.db import DBConnectionHandler


@pytest.fixture(scope="function")
def db():
    """
    Cria e fecha a conexão com o banco de dados.
    """

    now = (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%S")

    with DBConnectionHandler() as database:
        yield database

        database.session.execute(text(f"DELETE FROM users WHERE created_at__lde={now}"))
        database.session.commit()
