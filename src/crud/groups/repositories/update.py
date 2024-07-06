from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    update, Update,
    delete, Delete,
    insert, Insert
)
from src.engines.logger import ProjectLoggerSingleton
from src.crud.permissions.dtos import RetrievePermissionInputDTO
from src.crud.permissions.repositories import RetrievePermissionDAO
from ..models import Group, GroupsVsPermissions
from ..dtos import UpdateGroupInputDTO


class UpdateGroupDAO:
    """
    Repositorio de manipulação da entidade de grupos
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def execute(self, _id: int, dto: UpdateGroupInputDTO, commit: bool = True) -> Optional[Group]:
        """
        Pega os dados de um grupo pelo _id e atualiza
        """

        permission_dao = RetrievePermissionDAO(session=self.session)
        statement: Update = update(Group).values(
            name=dto.name, updated_at=datetime.now()
        ).where(Group.id == _id).returning(Group)

        try:
            updated_group: Group = await self.session.scalar(statement)

            if dto.permissions is not None:
                statement: Delete = delete(GroupsVsPermissions).where(
                    GroupsVsPermissions.group_id == updated_group.id
                )
                await self.session.execute(statement)

                for permission_code in dto.permissions:
                    permission = await permission_dao.retrieve(
                        dto=RetrievePermissionInputDTO(code=permission_code)
                    )
                    if permission:
                        statement: Insert = insert(GroupsVsPermissions).values(
                            group_id=updated_group.id,
                            permission_id=permission.id
                        )
                        await self.session.execute(statement)

            if commit:
                await self.session.commit()
                self.logger.info("Grupo atualizado no banco.")
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao atualizar o grupo: {e}")
            await self.session.rollback()
            raise e

        return updated_group
