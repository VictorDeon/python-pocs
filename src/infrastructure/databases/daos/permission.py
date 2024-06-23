import logging
from typing import Optional, Any
from sqlalchemy import or_, and_
from sqlalchemy.orm.exc import NoResultFound
from src.adapters.dtos import CreatePermissionInputDTO, ListPermissionInputDTO
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

        with DBConnectionHandler.connect(close_session) as database:
            try:
                database.session.add(permission)
                if commit:
                    database.session.commit()
                logging.info(f"Permissão {permission.name} criado com sucesso.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar a permissão: {e}")
                database.session.rollback()
                database.close_session(True)
                raise e

        return permission

    async def list(self, dto: ListPermissionInputDTO, close_session: bool = True) -> list[Permission]:
        """
        Pega uma lista de objetos.
        """

        permissions: list[Permission] = []
        with DBConnectionHandler.connect(close_session) as database:
            if dto.name and dto.code:
                condition = or_(
                    Permission.name.like(f"%{dto.name}%"),
                    Permission.code == dto.code
                )
            elif dto.name:
                condition = and_(Permission.name.like(f"%{dto.name}%"))
            elif dto.code:
                condition = and_(Permission.code == dto.code)

            try:
                permissions = database.session \
                    .query(Permission) \
                    .with_entities(
                        Permission.id,
                        Permission.name,
                        Permission.code
                    ) \
                    .filter(condition) \
                    .all()
            except Exception as e:
                logging.error(f"Ocorreu um problema ao listar as permissões: {e}")
                database.close_session(True)
                raise e

        return permissions

    async def get_by_id(self, _id: int, close_session: bool = True) -> Optional[Permission]:
        """
        Pega os dados de uma permissão pelo _id
        """

        permission: Permission = None
        with DBConnectionHandler.connect(close_session) as database:
            try:
                permission = database.session.query(Permission).get(_id)
            except Exception as e:
                logging.error(f"Ocorreu um problema ao pegar os dados da permissão: {e}")
                database.close_session(True)
                raise e

        return permission

    async def retrieve(self, dto: Any, close_session: bool = True) -> Optional[Permission]:
        """
        Pega os dados de uma permissão pelo _id
        """

        permission: Permission = None
        with DBConnectionHandler.connect(close_session) as database:
            try:
                permission = database.session \
                    .query(Permission) \
                    .filter(Permission.code == dto.code) \
                    .one()
            except NoResultFound as e:
                logging.warn(f"Permissão com código {dto.code} não encontrada: {e}")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao pegar os dados da permissão: {e}")
                database.close_session()
                raise e

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
        with DBConnectionHandler.connect(close_session) as database:
            try:
                permission = database.session.query(Permission).filter(Permission.id == _id).update(dto.to_dict())
                if commit:
                    database.session.commit()
            except Exception as e:
                logging.error(f"Ocorreu um problema ao atualizar a permissão: {e}")
                database.session.rollback()
                database.close_session()
                raise e

        return permission

    async def delete(
        self,
        _id: int,
        commit: bool = True,
        close_session: bool = True) -> None:
        """
        Pega os dados de uma permissão pelo _id
        """

        with DBConnectionHandler.connect(close_session) as database:
            try:
                database.session.query(Permission).filter(Permission.id == _id).delete()
                if commit:
                    database.session.commit()
            except Exception as e:
                logging.error(f"Ocorreu um problema ao deletar a permissão: {e}")
                database.session.rollback()
                database.close_session()
                raise e

    async def count(self, close_session: bool = True) -> int:
        """
        Pega a quantidade de permissões registros no banco.
        """

        qtd: int = 0
        with DBConnectionHandler.connect(close_session) as database:
            try:
                qtd = database.session.query(Permission).count()
            except Exception as e:
                logging.error(f"Ocorreu um problema ao realizar a contagem de permissões: {e}")
                database.close_session()
                raise e

        return qtd
