from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from sqlalchemy import select, Select
from ..models import Group


class RetrieveGroupDAO:
    """
    Repositorio de manipulação da entidade de grupos
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def get_by_id(self, _id: int) -> Optional[Group]:
        """
        Pega os dados de um grupo pelo _id
        """

        statement: Select = select(Group).where(Group.id == _id)
        try:
            group: Group = await self.session.scalar(statement)
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao pegar os dados do grupo: {e}")
            raise e

        return group
