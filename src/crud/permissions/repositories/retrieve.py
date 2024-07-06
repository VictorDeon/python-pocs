from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from sqlalchemy import select, Select
from ..dtos import RetrievePermissionInputDTO
from ..models import Permission


class RetrievePermissionDAO:
    """
    Repositorio de manipulação da entidade de permissão
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def get_by_id(self, _id: int) -> Optional[Permission]:
        """
        Pega os dados de uma permissão pelo _id
        """

        statement = select(Permission).where(Permission.id == _id)
        try:
            permission: Permission = await self.session.scalar(statement)
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao pegar os dados da permissão: {e}")
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
            self.logger.error(f"Ocorreu um problema ao pegar os dados da permissão: {e}")
            raise e

        return permission
