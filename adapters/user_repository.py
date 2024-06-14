import logging
from collections import namedtuple
from engines.db import DBConnectionHandler
from entities import User as EntityUser
from .repository import Repository


class UserRepository(Repository):
    """
    Repositorio de manipulação da entidade user
    """

    User = namedtuple("User", "id, name, email")

    @classmethod
    def create(cls, email: str, name: str, password: str) -> User:
        """
        Cria o usuário passando como argumento os dados do mesmo.
        """

        user = None
        with DBConnectionHandler() as database:
            try:
                new_user = EntityUser(
                    name=name,
                    email=email,
                    password=password
                )
                database.session.add(new_user)
                database.session.commit()
                user = cls.User(id=new_user.id, name=new_user.name, email=new_user.email)
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar o usuário: {e}")
                database.session.rollback()
                raise e
            finally:
                database.session.close()

        return user
