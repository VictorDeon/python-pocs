import logging
from src.infrastructure.databases.connection import DBConnectionHandler
from src.infrastructure.databases.models import (
    User,
    Profile,
    Permission,
    Group,
    Company
)
from src.infrastructure.databases.interfaces import UserDAOInterface


class UserDAO(UserDAOInterface):
    """
    Repositorio de manipulação da entidade user
    """

    async def create(
        self,
        email: str,
        name: str,
        password: str,
        phone: str = None,
        address: str = None,
        work_company: Company = None,
        groups: list[Group] = [],
        permissions: list[Permission] = []) -> User:
        """
        Cria o usuário passando como argumento os dados do mesmo.
        """

        profile = Profile(phone=phone, address=address)

        user = User(
            name=name,
            email=email,
            password=password,
            profile=profile,
            work_company=work_company,
            groups=groups,
            permissions=permissions
        )

        with DBConnectionHandler() as database:
            try:
                database.session.add(user)
                database.session.commit()
                logging.info(f"Usuário {user.name} criado com sucesso.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar o usuário: {e}")
                database.session.rollback()
                raise e
            finally:
                database.session.close()

        return user

    async def retrieve(self, _id: int) -> User:
        """
        Pesquisa o usuário pelo email.
        """

        user: User = None
        with DBConnectionHandler() as database:
            try:
                user = database.session.query(User).get(_id)
            except Exception as e:
                logging.error(f"Ocorreu um problema ao buscar o usuário: {e}")
                raise e
            finally:
                database.session.close()

        return user

    async def list(self, email: int = None) -> list[User]:
        """
        Pesquisa o usuário pelo email.
        """

        users: list[User] = []
        with DBConnectionHandler() as database:
            try:
                users = database.session.query(User).filter(
                    User.email == email
                )
            except Exception as e:
                logging.error(f"Ocorreu um problema ao buscar o usuário: {e}")
                raise e
            finally:
                database.session.close()

        return users
