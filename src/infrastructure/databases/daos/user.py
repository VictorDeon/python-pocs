import logging
from src.adapters.dtos.create_user import CreateUserInputDTO
from src.infrastructure.databases.connection import DBConnectionHandler
from src.infrastructure.databases.models import User, Profile
from src.infrastructure.databases.interfaces import UserDAOInterface


class UserDAO(UserDAOInterface):
    """
    Repositorio de manipulação da entidade user
    """

    async def create(self, user: CreateUserInputDTO) -> User:
        """
        Cria o usuário passando como argumento os dados do mesmo.
        """

        profile = Profile(**user.profile.to_dict())

        groups = []
        for group_id in user.groups:
            logging.info(f"Buscar o grupo {group_id} e adicionar na lista de grupos.")

        permissions = []
        for permission_id in user.permissions:
            logging.info(f"Buscar a permissão {permission_id} e adicionar na lista de permissões")

        user = User(
            **user.to_dict(),
            profile=profile,
            work_company=user.work_company_cnpj,
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

    async def retrieve(self, id: int) -> User:
        """
        Pesquisa o usuário pelo email.
        """

        user: User = None
        with DBConnectionHandler() as database:
            try:
                user = database.session.query(User).get(id)
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
