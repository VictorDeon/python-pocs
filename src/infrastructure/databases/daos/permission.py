import logging
from typing import Optional
from sqlalchemy import select, Select, insert, Insert, func, update, Update, delete, Delete
from src.adapters.dtos import (
    CreatePermissionInputDTO, ListPermissionInputDTO,
    RetrievePermissionInputDTO, UpdatePermissionInputDTO
)
from src.domains.utils.exceptions import GenericException
from src.infrastructure.databases.models import Permission, GroupsVsPermissions
from src.infrastructure.databases import DAOInterface


class PermissionDAO(DAOInterface):
    """
    Repositorio de manipulação da entidade de permissão
    """

    async def create(self, dto: CreatePermissionInputDTO, commit: bool = True) -> Permission:
        """
        Cria a permissão passando como argumento os dados da mesma.
        """

        try:
            statement: Insert = insert(Permission).values(**dto.to_dict()).returning(Permission)
            permission: Permission = await self.session.scalar(statement)
            if commit:
                await self.session.commit()
                logging.info("Permissões inseridadas no banco.")
        except Exception as e:
            logging.error(f"Ocorreu um problema ao criar a permissão: {e}")
            await self.session.rollback()
            raise e

        return permission

    async def list(self, dto: ListPermissionInputDTO) -> list[Permission]:
        """
        Pega uma lista de objetos.
        """

        statement: Select = select(Permission)

        if dto:
            if dto.group_id:
                statement: Select = statement \
                    .join(GroupsVsPermissions, GroupsVsPermissions.permission_id == Permission.id) \
                    .where(GroupsVsPermissions.group_id == dto.group_id)

            if dto.name:
                statement: Select = statement.where(Permission.name.like(f"%{dto.name}%"))

            if dto.code:
                statement: Select = statement.where(Permission.code == dto.code)

        try:
            result = await self.session.scalars(statement=statement)
            permissions: list[Permission] = result.all()
        except Exception as e:
            logging.error(f"Ocorreu um problema ao listar as permissões: {e}")
            raise e

        return permissions

    async def get_by_id(self, _id: int) -> Optional[Permission]:
        """
        Pega os dados de uma permissão pelo _id
        """

        statement = select(Permission).where(Permission.id == _id)
        try:
            permission: Permission = await self.session.scalar(statement)
        except Exception as e:
            logging.error(f"Ocorreu um problema ao pegar os dados da permissão: {e}")
            raise e

        return permission

    async def retrieve(self, dto: RetrievePermissionInputDTO) -> Optional[Permission]:
        """
        Pega os dados de uma permissão pelo _id
        """

        statement: Select = select(Permission).where(Permission.code == dto.code)

        try:
            permission: Permission = await self.session.scalar(statement)
        except Exception as e:
            logging.error(f"Ocorreu um problema ao pegar os dados da permissão: {e}")
            raise e

        return permission

    async def update(self, _id: int, dto: UpdatePermissionInputDTO, commit: bool = True) -> Optional[Permission]:
        """
        Pega os dados de uma permissão pelo _id e atualiza
        """

        statement: Update = update(Permission) \
            .values(**dto.to_dict()) \
            .where(Permission.id == _id) \
            .returning(Permission)

        try:
            permission: Permission = await self.session.scalar(statement)
            if not permission:
                raise GenericException(f"Permissão com id {_id} não encontrado.")

            if commit:
                await self.session.commit()
                logging.info("Permissões atualizadas no banco.")
        except Exception as e:
            logging.error(f"Ocorreu um problema ao atualizar a permissão: {e}")
            await self.session.rollback()
            raise e

        return permission

    async def delete(self, _id: int, commit: bool = True) -> int:
        """
        Pega os dados de uma permissão pelo _id e deleta
        """

        statement: Delete = delete(Permission).where(Permission.id == _id).returning(Permission.id)
        try:
            permission_id: int = await self.session.scalar(statement)
            if not permission_id:
                raise GenericException(f"Permissão com id {_id} não encontrado.")

            if commit:
                await self.session.commit()
                logging.info("Permissões deletadas do banco.")
        except Exception as e:
            logging.error(f"Ocorreu um problema ao deletar a permissão: {e}")
            await self.session.rollback()
            raise e

        return permission_id

    async def count(self) -> int:
        """
        Pega a quantidade de permissões registradas no banco.
        """

        statement = select(func.count(Permission.id))
        try:
            qtd: int = await self.session.scalar(statement)
        except Exception as e:
            logging.error(f"Ocorreu um problema ao realizar a contagem de permissões: {e}")
            raise e

        return qtd
