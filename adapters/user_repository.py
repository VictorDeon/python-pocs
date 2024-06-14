from engines.db import DBConnectionHandler
from entities import User
from .repository import Repository
import logging


class UserRepository(Repository):
    """
    Repositorio de manipulação da entidade user
    """

    @classmethod
    def create(cls,  *args, **kwargs) -> User:
        """
        Cria o usuário passando como argumento os dados do mesmo.
        """

        with DBConnectionHandler() as db_connection:
            try:
                new_user = User(*args, **kwargs)
                db_connection.session.add(new_user)
                db_connection.session.commit()
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar o usuário: {e}")
                db_connection.session.rollback()
                raise e
            finally:
                db_connection.session.close()

        return new_user
