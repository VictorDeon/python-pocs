import logging
from typing import Optional, Any
from src.adapters.dtos import CreatePermissionInputDTO
from src.infrastructure.databases.connection import DBConnectionHandler
from src.infrastructure.databases.models import Permission
from src.infrastructure.databases import DAOInterface


class PermissionDAO(DAOInterface):
    """
    Repositorio de manipulação da entidade de permissão
    """

    async def create(
        self,
        dto: CreatePermissionInputDTO,
        commit: bool = True,
        close_session: bool = True) -> Permission:
        """
        Cria a permissão passando como argumento os dados da mesma.
        """

        permission = Permission(**dto.to_dict())

        with DBConnectionHandler() as database:
            try:
                database.session.add(permission)
                if commit:
                    database.session.commit()
                logging.info(f"Permissão {permission.name} criado com sucesso.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar a permissão: {e}")
                database.session.rollback()
                raise e
            finally:
                if close_session:
                    database.session.close()

        return permission

    async def list(self, dto: Any, close_session: bool = True) -> list[Permission]:
        """
        Pega uma lista de objetos.
        """

        permissions: list[Permission] = []
        with DBConnectionHandler() as database:
            try:
                permissions = database.session.query(Permission).filter(
                    Permission.name == dto.name or
                    Permission.code == dto.code
                )
            except Exception as e:
                logging.error(f"Ocorreu um problema ao listar as permissões: {e}")
                raise e
            finally:
                if close_session:
                    database.session.close()

        return permissions


    async def retrieve(self, _id: int, close_session: bool = True) -> Optional[Permission]:
        """
        Pega os dados de uma permissão pelo _id
        """

        permission: Permission = None
        with DBConnectionHandler() as database:
            try:
                permission = database.session.query(Permission).get(_id)
            except Exception as e:
                logging.error(f"Ocorreu um problema ao pegar os dados da permissão: {e}")
                raise e
            finally:
                if close_session:
                    database.session.close()

        return permission

    async def update(
        self,
        _id: int,
        dto: Any,
        commit: bool = True,
        close_session: bool = True) -> Optional[Permission]:
        """
        Pega os dados de uma permissão pelo _id
        """

        permission: Permission = None
        with DBConnectionHandler() as database:
            try:
                permission = database.session.query(Permission).filter(Permission.id == _id).update(dto.to_dict())
                if commit:
                    database.session.commit()
            except Exception as e:
                logging.error(f"Ocorreu um problema ao atualizar a permissão: {e}")
                database.session.rollback()
                raise e
            finally:
                if close_session:
                    database.session.close()

        return permission

    async def delete(
        self,
        _id: int,
        commit: bool = True,
        close_session: bool = True) -> None:
        """
        Pega os dados de uma permissão pelo _id
        """

        with DBConnectionHandler() as database:
            try:
                database.session.query(Permission).filter(Permission.id == _id).delete()
                if commit:
                    database.session.commit()
            except Exception as e:
                logging.error(f"Ocorreu um problema ao deletar a permissão: {e}")
                database.session.rollback()
                raise e
            finally:
                if close_session:
                    database.session.close()

    async def count(self, close_session: bool = True) -> int:
        """
        Pega a quantidade de permissões registros no banco.
        """

        qtd: int = 0
        with DBConnectionHandler() as database:
            try:
                qtd = database.session.query(Permission).count()
            except Exception as e:
                logging.error(f"Ocorreu um problema ao realizar a contagem de permissões: {e}")
                raise e
            finally:
                if close_session:
                    database.session.close()

        return qtd
