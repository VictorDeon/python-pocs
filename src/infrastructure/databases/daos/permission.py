import logging
from typing import Optional
from sqlalchemy import select, Select, insert, Insert, func, update, Update, delete, Delete
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

        async with DBConnectionHandler.connect(close_session) as database:
            try:
                values = dto.to_dict()
                statement: Insert = insert(Permission).values(**values).returning(Permission)
                logging.debug(f"{statement} = {values}")
                permission: Permission = await database.session.scalar(statement)
                if commit:
                    await database.session.commit()
                    logging.info("Permissões inseridadas no banco.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao criar a permissão: {e}")
                await database.session.rollback()
                database.close_session(True)
                raise e

        return permission

    async def list(self, dto: ListPermissionInputDTO, close_session: bool = True) -> list[Permission]:
        """
        Pega uma lista de objetos.
        """

        permissions: list[Permission] = []
        async with DBConnectionHandler.connect(close_session) as database:
            statement: Select = select(Permission)

            if dto:
                if dto.name:
                    statement: Select = statement.where(Permission.name.like(f"%{dto.name}%"))

                if dto.code:
                    statement: Select = statement.where(Permission.code == dto.code)

            try:
                logging.debug(statement)
                result = await database.session.scalars(statement=statement)
                permissions = result.all()
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
        async with DBConnectionHandler.connect(close_session) as database:
            statement = select(Permission).where(Permission.id == _id)
            try:
                logging.debug(statement)
                permission = await database.session.scalar(statement)
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
        async with DBConnectionHandler.connect(close_session) as database:
            statement: Select = select(Permission).where(Permission.code == dto.code)

            try:
                logging.debug(statement)
                permission = await database.session.scalar(statement)
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
        Pega os dados de uma permissão pelo _id e atualiza
        """

        permission: Permission = None
        async with DBConnectionHandler.connect(close_session) as database:
            statement: Update = update(Permission) \
                .values(**dto.to_dict()) \
                .where(Permission.id == _id) \
                .returning(Permission)

            logging.debug(statement)

            try:
                permission: Permission = await database.session.execute(statement)
                if commit:
                    await database.session.commit()
                    logging.info("Permissões atualizadas no banco.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao atualizar a permissão: {e}")
                await database.session.rollback()
                database.close_session()
                raise e

        return permission

    async def delete(
        self,
        _id: int,
        commit: bool = True,
        close_session: bool = True) -> int:
        """
        Pega os dados de uma permissão pelo _id e deleta
        """

        async with DBConnectionHandler.connect(close_session) as database:
            statement: Delete = delete(Permission).where(Permission.id == _id).returning(Permission.id)
            logging.debug(statement)
            try:
                permission_id: int = await database.session.scalar(statement)
                if commit:
                    await database.session.commit()
                    logging.info("Permissões deletadas do banco.")
            except Exception as e:
                logging.error(f"Ocorreu um problema ao deletar a permissão: {e}")
                await database.session.rollback()
                database.close_session()
                raise e

        return permission_id

    async def count(self, close_session: bool = True) -> int:
        """
        Pega a quantidade de permissões registradas no banco.
        """

        qtd: int = 0
        async with DBConnectionHandler.connect(close_session) as database:
            statement = select(func.count(Permission.id))
            try:
                qtd = await database.session.scalar(statement)
            except Exception as e:
                logging.error(f"Ocorreu um problema ao realizar a contagem de permissões: {e}")
                database.close_session()
                raise e

        return qtd
