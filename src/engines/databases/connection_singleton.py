import os
import time
from typing import Optional
from pathlib import Path
from fastapi import HTTPException
from sqlalchemy import event, Engine
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker,
    AsyncSession, AsyncEngine
)
from src.engines.logger import ProjectLoggerSingleton

logger = ProjectLoggerSingleton.get_logger()


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """
    Executado antes da consulta SQL
    """

    context._query_start_time = time.time()
    logger.debug("Start Query:\n%s" % statement)
    logger.debug("Parameters: %r" % (parameters,))


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """
    Executado após a consulta SQL
    """

    total = time.time() - context._query_start_time
    logger.debug("Query Complete! Total Time: %.02fms" % (total * 1000))


class DBConnectionSingleton:
    """
    Client singleton de conexão com o banco.
    """

    __instance = None
    __connection_pool_expire = int(os.environ.get("DB_CONNECTION_EXPIRE", 120))

    def __init__(self) -> None:
        """
        Construtor.
        """

        if self.__instance:
            raise HTTPException(status_code=500, detail="Não se pode instânciar uma classe singleton.")

        logger.info("Abrindo a pool de conexões")
        self.__connection_pool_started = time.time()
        self.__connection_string: Optional[str] = os.environ.get("DB_CONNECTION_STRING")
        self.__engine: Optional[AsyncEngine] = None
        if not self.__connection_string or self.__connection_string.startswith("sqlite"):
            engine = self.__create_engine(sqlite=True)
        else:
            engine = self.__create_engine()

        self.__create_session(engine)

    @classmethod
    async def get_instance(cls) -> "DBConnectionSingleton":
        """
        Realiza a conexão do singleton e retorna a sessão do banco de dados.
        """

        if not cls.__instance:
            cls.__instance = DBConnectionSingleton()

        connection_pool_time = time.time() - cls.__instance.__connection_pool_started
        logger.info(f"Ja se passaram {connection_pool_time:.2f} ms no pool de conexões do DB.")
        if connection_pool_time >= cls.__connection_pool_expire:
            await cls.__instance.session.close()
            cls.__instance = None
            cls.__instance = DBConnectionSingleton()

        return cls.__instance

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
        logger.debug("DB pool de conexões iniciado.")
