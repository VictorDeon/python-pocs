# pylint: disable=invalid-name

import os
from typing import Optional
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.future.engine import Engine
from src.infrastructure.databases import BaseModel


class DBConnectionHandler:
    """
    Realiza a lógica de conexão com o banco de dados usando SQL ALQUEMY.
    """

    def __init__(self) -> None:
        """
        Construtor.
        """

        self.__connection_string: Optional[str] = os.environ.get("DB_CONNECTION_STRING")
        self.__engine: Optional[Engine] = None
        self.session = None

    def __create_engine(self, sqlite: bool = False) -> Engine:
        """
        Cria a engine de execução do sqlalchemy.
        """

        if self.__engine:
            return self.__engine

        if sqlite:
            db_path = "poc.sqlite"
            folder = Path(db_path).parent
            folder.mkdir(parents=True, exist_ok=True)
            connection_string = f"sqlite:///{db_path}"
            self.__engine = create_engine(url=connection_string, echo=False, connect_args={"check_same_thread": False})
        else:
            self.__engine = create_engine(url=self.__connection_string, echo=False)

        return self.__engine

    def __create_session(self, engine: Engine) -> Session:
        """
        Cria a sessão de conexão do banco de dados.
        """

        __session = sessionmaker(bind=engine, expire_on_commit=False, class_=Session)
        self.session: Session = __session()

    def create_tables(self):
        """
        Cria uma tabela no banco de dados.
        """

        import src.infrastructure.databases.models
        BaseModel.metadata.drop_all(self.__engine)
        BaseModel.metadata.create_all(self.__engine)

    def __enter__(self):
        """
        Executado ao criar um contexto com o with.
        """

        if not self.__connection_string or self.__connection_string.startswith("sqlite"):
            engine = self.__create_engine(sqlite=True)
        else:
            engine = self.__create_engine()

        self.__create_session(engine)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Executado ao sair de um contexto with.
        """

        self.session.close()
