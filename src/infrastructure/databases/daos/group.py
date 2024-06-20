import logging
from src.infrastructure.databases.connection import DBConnectionHandler
from src.infrastructure.databases.models import Group, Permission
from src.infrastructure.databases.interfaces import UserDAOInterface


class GroupDAO(UserDAOInterface):
    """
    Repositorio de manipulação da entidade group
    """

    async def create(self, name: str, permissions: list[Permission]) -> Group:
        """
        Cria o grupo passando como argumento os dados do mesmo.
        """


        group = Group(
            name=name,
            permissions=permissions
        )

        with DBConnectionHandler() as database:
            try:
                database.session.add(group)
                database.session.commit()
                logging.info(f"Grupo {group.name} criado com sucesso.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar o grupo: {e}")
                database.session.rollback()
                raise e
            finally:
                database.session.close()

        return group
