from sqlalchemy import delete, Delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from src.crud.users.models import UsersVsGroups
from ..models import Group, GroupsVsPermissions


class DeleteGroupDAO:
    """
    Repositorio de manipulação da entidade de grupos
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def execute(self, _id: int, commit: bool = True) -> int:
        """
        Pega os dados de um grupo pelo _id
        """

        try:
            statement: Delete = delete(UsersVsGroups).where(UsersVsGroups.group_id == _id)
            await self.session.execute(statement)

            statement: Delete = delete(GroupsVsPermissions).where(GroupsVsPermissions.group_id == _id)
            await self.session.execute(statement)

            statement: Delete = delete(Group).where(Group.id == _id).returning(Group.id)

            group_id: int = await self.session.scalar(statement)
            if commit:
                await self.session.commit()
                self.logger.info("Grupos deletadas do banco.")
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao deletar o grupo: {e}")
            await self.session.rollback()
            raise e

        return group_id
