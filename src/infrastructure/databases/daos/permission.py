import logging
from src.adapters.dtos import CreatePermissionInputDTO
from src.infrastructure.databases.connection import DBConnectionHandler
from src.infrastructure.databases.models import Permission
from src.infrastructure.databases import DAOInterface


class PermissionDAO(DAOInterface):
    """
    Repositorio de manipulação da entidade de permissão
    """

    async def create(self, dto: CreatePermissionInputDTO) -> Permission:
        """
        Cria a permissão passando como argumento os dados da mesma.
        """

        permission = Permission(**dto.to_dict())

        with DBConnectionHandler() as database:
            try:
                database.session.add(permission)
                database.session.commit()
                logging.info(f"Permissão {permission.name} criado com sucesso.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar a permissão: {e}")
                database.session.rollback()
                raise e
            finally:
                database.session.close()

        return permission
