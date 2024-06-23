import os
import logging
from typing import Optional, Any
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.future.engine import Engine
from src.infrastructure.databases import BaseModel


class DBConnectionHandler:
    """
    Realiza a lógica de conexão com o banco de dados usando SQL ALQUEMY.
    """

    __instance = None

    def __init__(self, close_session: bool = True) -> None:
        """
        Construtor.
        """

        self.__connection_string: Optional[str] = os.environ.get("DB_CONNECTION_STRING")
        self.__engine: Optional[Engine] = None
        self.__close_session = close_session
        self.session = None

    @classmethod
    def connect(cls, close_session: bool = True):
        """
        Realiza a conexão.
        """

        if not cls.__instance:
            cls.__instance = DBConnectionHandler(close_session)

        cls.__instance.__close_session = close_session
        return cls.__instance

    def close_session(self, value: bool = True) -> None:
        """
        Configura o fechamento de conexão.
        """

        self.__close_session = value

    def __create_engine(self, sqlite: bool = False) -> Engine:
        """
        Cria a engine de execução do sqlalchemy.
        """

        if self.__engine:
            return self.__engine

        echo = os.environ.get("APP_ENV") == "tests"

        if sqlite:
            db_path = "assets/db/poc.sqlite"
            folder = Path(db_path).parent
            folder.mkdir(parents=True, exist_ok=True)
            connection_string = f"sqlite:///{db_path}"
            self.__engine = create_engine(url=connection_string, echo=echo, connect_args={"check_same_thread": False})
        else:
            self.__engine = create_engine(url=self.__connection_string, echo=echo)

        return self.__engine

    def __create_session(self, engine: Engine) -> Session:
        """
        Cria a sessão de conexão do banco de dados.
        """

        __session = sessionmaker(bind=engine, expire_on_commit=False, class_=Session)
        self.session: Session = __session()
        logging.debug("DB pool de conexões iniciado.")

    def create_tables(self):
        """
        Cria uma tabela no banco de dados.
        """

        import src.infrastructure.databases.models  # noqa: F401
        BaseModel.metadata.drop_all(self.__engine)
        BaseModel.metadata.create_all(self.__engine)

    def __enter__(self):
        """
        Executado ao criar um contexto com o with.
        """

        if self.session:
            return self

        if not self.__connection_string or self.__connection_string.startswith("sqlite"):
            engine = self.__create_engine(sqlite=True)
        else:
            engine = self.__create_engine()

        self.__create_session(engine)

        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Executado ao sair de um contexto with.
        """

        if self.__close_session:
            self.session.close()
            self.session = None
            self.__instance = None
            logging.debug("DB pool de conexões finalizada.")
