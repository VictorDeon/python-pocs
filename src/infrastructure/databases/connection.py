import os
import logging
from typing import Optional, Any
from pathlib import Path
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker,
    AsyncSession, AsyncEngine
)


class DBConnectionHandler:
    """
    Realiza a lógica de conexão com o banco de dados usando SQL ALQUEMY.
    """

    def __init__(self) -> None:
        """
        Construtor.
        """

        self.__connection_string: Optional[str] = os.environ.get("DB_CONNECTION_STRING")
        self.__engine: Optional[AsyncEngine] = None
        self.session = None

    def __create_engine(self, sqlite: bool = False) -> AsyncEngine:
        """
        Cria a engine de execução do sqlalchemy.
        """

        if self.__engine:
            return self.__engine

        if sqlite:
            db_path = "assets/db/poc.sqlite"
            folder = Path(db_path).parent
            folder.mkdir(parents=True, exist_ok=True)
            connection_string = f"sqlite:///{db_path}"
            self.__engine = create_async_engine(url=connection_string, echo=False, connect_args={"check_same_thread": False})
        else:
            self.__engine = create_async_engine(url=self.__connection_string, echo=False)

        return self.__engine

    def __create_session(self, engine: AsyncEngine) -> AsyncSession:
        """
        Cria a sessão de conexão do banco de dados.
        """

        __session = async_sessionmaker(bind=engine, expire_on_commit=False)
        self.session: AsyncSession = __session()
        logging.debug("DB pool de conexões iniciado.")

    async def __aenter__(self) -> "DBConnectionHandler":
        """
        Executado ao criar um contexto com o with.
        """

        if not self.__connection_string or self.__connection_string.startswith("sqlite"):
            engine = self.__create_engine(sqlite=True)
        else:
            engine = self.__create_engine()

        self.__create_session(engine)

        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Executado ao sair de um contexto with.
        """

        await self.session.close()
        self.session = None
        logging.debug("DB pool de conexões finalizada.")
