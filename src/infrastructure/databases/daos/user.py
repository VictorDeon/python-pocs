import logging
from src.domains.entities import User, Profile, Permission, Group
from src.infrastructure.databases.connection import DBConnectionHandler
from src.infrastructure.databases.models import (
    User as UserModel,
    Profile as ProfileModel,
    Permission as PermissionModel,
    Group as GroupModel,
    Company as CompanyModel
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
        work_company: CompanyModel = None,
        groups: list[GroupModel] = [],
        permissions: list[PermissionModel] = []) -> User:
        """
        Cria o usuário passando como argumento os dados do mesmo.
        """

        profile = ProfileModel(phone=phone, address=address)

        user = UserModel(
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

        return User(
            id=user.id,
            name=user.name,
            email=user.email,
            profile=Profile(**profile.__dict__),
            groups=[Group(**group) for group in user.groups],
            permissions=[Permission(**permission) for permission in user.permissions]
        )

    async def retrieve(self, _id: int) -> User:
        """
        Pesquisa o usuário pelo email.
        """

        user = None
        with DBConnectionHandler() as database:
            try:
                _user: UserModel = database.session.query(UserModel).get(_id)
                if _user:
                    user = User(id=_user.id, name=_user.name, email=_user.email)
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

        users = []
        with DBConnectionHandler() as database:
            try:
                _users: UserModel = database.session.query(UserModel).filter(
                    UserModel.email == email
                )
                for user in _users:
                    users.append(User(id=user.id, name=user.name, email=user.email))
            except Exception as e:
                logging.error(f"Ocorreu um problema ao buscar o usuário: {e}")
                raise e
            finally:
                database.session.close()

        return users
