import pytest
from sqlalchemy import text
from engines.db import DBConnectionHandler


@pytest.mark.skip(reason="Sensive test")
def test_create_database_engine():
    """
    Testando a criação da conexão com o banco de dados.
    """

    with DBConnectionHandler() as db_connector:
        result = db_connector.session.execute(text("select * from users"))
        assert len(result.fetchall()) > 0
