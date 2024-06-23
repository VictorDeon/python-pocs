import logging
from typing import Optional
from sqlalchemy import and_, select, Select
from sqlalchemy.orm.exc import NoResultFound
from src.adapters.dtos import (
    CreatePermissionInputDTO, ListPermissionInputDTO,
    RetrievePermissionInputDTO, UpdatePermissionInputDTO
)
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
                    logging.info("Permissões inseridadas no banco.")
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
            statement: Select = select(Permission)

            if dto:
                if dto.name and dto.code:
                    statement: Select = statement.where(Permission.name.like(f"%{dto.name}%"))
                    statement: Select = statement.where(Permission.code == dto.code)
                elif dto.name:
                    statement: Select = statement.where(Permission.name.like(f"%{dto.name}%"))
                elif dto.code:
                    statement: Select = statement.where(Permission.code == dto.code)

            try:
                permissions = database.session.scalars(statement=statement).all()
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
                permission = database.session.get(Permission, _id)
            except Exception as e:
                logging.error(f"Ocorreu um problema ao pegar os dados da permissão: {e}")
                database.close_session(True)
                raise e

        return permission

    async def retrieve(self, dto: RetrievePermissionInputDTO, close_session: bool = True) -> Optional[Permission]:
        """
        Pega os dados de uma permissão pelo _id
        """

        permission: Permission = None
        with DBConnectionHandler.connect(close_session) as database:
            statement: Select = select(Permission).where(Permission.code == dto.code)

            try:
                permission = database.session.scalars(statement).one()
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
        dto: UpdatePermissionInputDTO,
        commit: bool = True,
        close_session: bool = True) -> Optional[Permission]:
        """
        Pega os dados de uma permissão pelo _id
        """

        permission: Permission = None
        with DBConnectionHandler.connect(close_session) as database:
            statement = select(Permission).where(Permission.id == _id)

            try:
                permission = database.session.scalars(statement).one()
                permission.code = dto.code
                permission.name = dto.name
                if commit:
                    database.session.commit()
                    logging.info("Permissões atualizadas no banco.")
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
                permission = database.session.get(Permission, _id)
                if not permission:
                    raise ValueError(f"Permissão com o id {_id} não encontrado.")

                database.session.delete(permission)
                if commit:
                    database.session.commit()
                    logging.info("Permissões deletadas do banco.")
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
