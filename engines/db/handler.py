from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
import os


class DBConnectionHandler:
    """
    Realiza a lógica de conexão com o banco de dados usando SQL ALQUEMY.
    """

    def __init__(self):
        """
        Construtor.
        """

        self.__connection_string = os.environ.get("DB_CONNECTION_STRING")
        self.session = None

    def __enter__(self):
        """
        Executado ao criar um contexto com o with.
        """

        engine: Engine = create_engine(self.__connection_string)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Executado ao sair de um contexto with.
        """

        self.session.close()
