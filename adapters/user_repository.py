import logging
from collections import namedtuple
from typing import List
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

    @classmethod
    def retrieve(cls, id: int) -> User:
        """
        Pesquisa o usuário pelo email.
        """

        user = None
        with DBConnectionHandler() as database:
            try:
                _user: EntityUser = database.session.query(EntityUser).get(id)
                if _user:
                    user = cls.User(id=_user.id, name=_user.name, email=_user.email)
            except Exception as e:
                logging.error(f"Ocorreu um problema ao buscar o usuário: {e}")
                raise e
            finally:
                database.session.close()

        return user

    @classmethod
    def list(cls, email: int = None) -> List[User]:
        """
        Pesquisa o usuário pelo email.
        """

        users = []
        with DBConnectionHandler() as database:
            try:
                _users: EntityUser = database.session.query(EntityUser).filter(EntityUser.email == email)
                for user in _users:
                    users.append(cls.User(id=user.id, name=user.name, email=user.email))
            except Exception as e:
                logging.error(f"Ocorreu um problema ao buscar o usuário: {e}")
                raise e
            finally:
                database.session.close()

        return users
