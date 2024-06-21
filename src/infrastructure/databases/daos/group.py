import logging
from src.adapters.dtos import CreateGroupInputDTO
from src.infrastructure.databases.connection import DBConnectionHandler
from src.infrastructure.databases.models import Group
from src.infrastructure.databases import DAOInterface


class GroupDAO(DAOInterface):
    """
    Repositorio de manipulação da entidade group
    """

    async def create(self, dto: CreateGroupInputDTO) -> Group:
        """
        Cria o grupo passando como argumento os dados do mesmo.
        """


        group = Group(name=dto.name)

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
