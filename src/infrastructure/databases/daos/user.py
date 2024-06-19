import logging
from typing import List
from src.domains.entities import User
from src.infrastructure.databases.connection import DBConnectionHandler
from src.infrastructure.databases.models import User as EntityUser, Profile
from src.infrastructure.databases.interfaces import UserDAOInterface


class UserDAO(UserDAOInterface):
    """
    Repositorio de manipulação da entidade user
    """

    async def create(self, email: str, name: str, password: str) -> User:
        """
        Cria o usuário passando como argumento os dados do mesmo.
        """

        profile = Profile(phone="61992839444")

        new_user = EntityUser(
            name=name,
            email=email,
            password=password,
            profile=profile
        )

        with DBConnectionHandler() as database:
            try:
                database.session.add(new_user)
                database.session.commit()
                logging.info(f"Usuário {new_user.name} criado com sucesso.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar o usuário: {e}")
                database.session.rollback()
                raise e
            finally:
                database.session.close()

        return User(id=new_user.id, name=new_user.name, email=new_user.email)

    async def retrieve(self, _id: int) -> User:
        """
        Pesquisa o usuário pelo email.
        """

        user = None
        with DBConnectionHandler() as database:
            try:
                _user: EntityUser = database.session.query(EntityUser).get(_id)
                if _user:
                    user = User(id=_user.id, name=_user.name, email=_user.email)
            except Exception as e:
                logging.error(f"Ocorreu um problema ao buscar o usuário: {e}")
                raise e
            finally:
                database.session.close()

        return user

    async def list(self, email: int = None) -> List[User]:
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
                    users.append(User(id=user.id, name=user.name, email=user.email))
            except Exception as e:
                logging.error(f"Ocorreu um problema ao buscar o usuário: {e}")
                raise e
            finally:
                database.session.close()

        return users
