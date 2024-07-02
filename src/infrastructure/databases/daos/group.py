import logging
from typing import Optional
from sqlalchemy import (
    select, Select,
    func,
    update as sql_update, Update,
    delete as sql_delete, Delete,
    insert as sql_insert, Insert
)
from src.adapters.dtos import (
    CreateGroupInputDTO, ListGroupInputDTO,
    UpdateGroupInputDTO, RetrievePermissionInputDTO
)
from src.infrastructure.databases.models import Group, Permission, GroupsVsPermissions, UsersVsGroups
from src.infrastructure.databases import DAOInterface
from .permission import PermissionDAO


class GroupDAO(DAOInterface):
    """
    Repositorio de manipulação da entidade de grupos
    """

    async def create(self, dto: CreateGroupInputDTO, commit: bool = True) -> Group:
        """
        Cria o grupo passando como argumento os dados do mesmo.
        """

        permission_dao = PermissionDAO(session=self.session)
        statement: Insert = sql_insert(Group).values(name=dto.name).returning(Group)

        try:
            group: Group = await self.session.scalar(statement)

            for permission_code in dto.permissions:
                permission = await permission_dao.retrieve(
                    dto=RetrievePermissionInputDTO(code=permission_code)
                )
                if permission:
                    statement: Insert = sql_insert(GroupsVsPermissions).values(
                        group_id=group.id,
                        permission_id=permission.id
                    )
                    await self.session.execute(statement)

            if commit:
                await self.session.commit()
                logging.info("Grupo atualizado no banco.")
        except Exception as e:
            logging.error(f"Ocorreu um problema ao criar o grupo: {e}")
            await self.session.rollback()
            raise e

        return group

    async def list(self, dto: ListGroupInputDTO) -> list[Group]:
        """
        Pega uma lista de grupos.
        """

        statement: Select = select(Group)

        if dto:
            if dto.user_id:
                statement: Select = statement \
                    .join(UsersVsGroups, UsersVsGroups.group_id == Group.id) \
                    .where(UsersVsGroups.user_id == dto.user_id)

            if dto.code:
                statement: Select = statement \
                    .join(GroupsVsPermissions, GroupsVsPermissions.group_id == Group.id) \
                    .join(Permission, Permission.id == GroupsVsPermissions.permission_id) \
                    .where(Permission.code == dto.code)

            if dto.name:
                statement: Select = statement.where(Group.name.like(f"%{dto.name}%"))

        try:
            result = await self.session.scalars(statement=statement)
            groups: list[Group] = result.all()
        except Exception as e:
            logging.error(f"Ocorreu um problema ao listar os grupos: {e}")
            raise e

        return groups

    async def get_by_id(self, _id: int) -> Optional[Group]:
        """
        Pega os dados de um grupo pelo _id
        """

        statement = select(Group).where(Group.id == _id)
        try:
            group: Group = await self.session.scalar(statement)
        except Exception as e:
            logging.error(f"Ocorreu um problema ao pegar os dados do grupo: {e}")
            raise e

        return group

    async def update(self, _id: int, dto: UpdateGroupInputDTO, commit: bool = True) -> Optional[Group]:
        """
        Pega os dados de um grupo pelo _id e atualiza
        """

        permission_dao = PermissionDAO(session=self.session)
        statement: Update = sql_update(Group).values(name=dto.name).where(Group.id == _id).returning(Group)

        try:
            updated_group: Group = await self.session.scalar(statement)

            if dto.permissions is not None:
                statement: Delete = sql_delete(GroupsVsPermissions).where(
                    GroupsVsPermissions.group_id == updated_group.id
                )
                await self.session.execute(statement)

                for permission_code in dto.permissions:
                    permission = await permission_dao.retrieve(
                        dto=RetrievePermissionInputDTO(code=permission_code)
                    )
                    if permission:
                        statement: Insert = sql_insert(GroupsVsPermissions).values(
                            group_id=updated_group.id,
                            permission_id=permission.id
                        )
                        await self.session.execute(statement)

            if commit:
                await self.session.commit()
                logging.info("Grupo atualizado no banco.")
        except Exception as e:
            logging.error(f"Ocorreu um problema ao atualizar o grupo: {e}")
            await self.session.rollback()
            raise e

        return updated_group

    async def delete(self, _id: int, commit: bool = True) -> int:
        """
        Pega os dados de um grupo pelo _id
        """

        try:
            statement: Delete = sql_delete(UsersVsGroups).where(UsersVsGroups.group_id == _id)
            await self.session.execute(statement)

            statement: Delete = sql_delete(GroupsVsPermissions).where(GroupsVsPermissions.group_id == _id)
            await self.session.execute(statement)

            statement: Delete = sql_delete(Group).where(Group.id == _id)
            await self.session.execute(statement)
            if commit:
                await self.session.commit()
                logging.info("Grupos deletadas do banco.")
        except Exception as e:
            logging.error(f"Ocorreu um problema ao deletar o grupo: {e}")
            await self.session.rollback()
            raise e

    async def count(self) -> int:
        """
        Pega a quantidade de grupos registrados no banco.
        """

        statement = select(func.count(Group.id))

        try:
            qtd = await self.session.scalar(statement)
        except Exception as e:
            logging.error(f"Ocorreu um problema ao realizar a contagem de grupos: {e}")
            raise e

        return qtd
