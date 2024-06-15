import logging
from collections import namedtuple
from typing import List
from engines.db import DBConnectionHandler
from engines.db.entities import User as EntityUser
from .repository import Repository


class UserRepository(Repository):
    """
    Repositorio de manipulação da entidade user
    """

    User = namedtuple("User", "id, name, email")

    def create(self, email: str, name: str, password: str) -> User:
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
                user = self.User(id=new_user.id, name=new_user.name, email=new_user.email)
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar o usuário: {e}")
                database.session.rollback()
                raise e
            finally:
                database.session.close()

        return user

    def retrieve(self, _id: int) -> User:
        """
        Pesquisa o usuário pelo email.
        """

        user = None
        with DBConnectionHandler() as database:
            try:
                _user: EntityUser = database.session.query(EntityUser).get(_id)
                if _user:
                    user = self.User(id=_user.id, name=_user.name, email=_user.email)
            except Exception as e:
                logging.error(f"Ocorreu um problema ao buscar o usuário: {e}")
                raise e
            finally:
                database.session.close()

        return user

    def list(self, email: int = None) -> List[User]:
        """
        Pesquisa o usuário pelo email.
        """

        users = []
        with DBConnectionHandler() as database:
            try:
                _users: EntityUser = database.session.query(EntityUser).filter(
                    EntityUser.email == email
                )
                for user in _users:
                    users.append(self.User(id=user.id, name=user.name, email=user.email))
            except Exception as e:
                logging.error(f"Ocorreu um problema ao buscar o usuário: {e}")
                raise e
            finally:
                database.session.close()

        return users

    def update(self, *args, **kwargs):
        """
        Atualização de um objeto.
        """

        return None

    def delete(self, *args, **kwargs):
        """
        Deleção de um objeto.
        """

        return None
