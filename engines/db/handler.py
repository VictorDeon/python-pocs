from sqlalchemy import create_engine, Engine
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

    def get_engine(self) -> Engine:
        """
        Pega a engine do SQL Alquimy.
        """

        engine = create_engine(self.__connection_string)
        return engine