import logging
from src.domains.entities import Group, Permission
from src.infrastructure.databases.connection import DBConnectionHandler
from src.infrastructure.databases.models import (
    Group as GroupModel,
    Permission as PermissionModel
)
from src.infrastructure.databases.interfaces import UserDAOInterface


class GroupDAO(UserDAOInterface):
    """
    Repositorio de manipulação da entidade group
    """

    async def create(self, name: str, permissions: list[PermissionModel]) -> Group:
        """
        Cria o grupo passando como argumento os dados do mesmo.
        """


        group = GroupModel(
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

        return Group(
            id=group.id,
            name=group.name,
            permissions=[
                Permission(**permission) for permission in group.permissions
            ]
        )
