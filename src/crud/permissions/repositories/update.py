from typing import Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from sqlalchemy import update, Update
from src.shared.exceptions import GenericException
from ..dtos import UpdatePermissionInputDTO
from ..models import Permission


class UpdatePermissionDAO:
    """
    Repositorio de manipulação da entidade de permissão
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def execute(self, _id: int, dto: UpdatePermissionInputDTO, commit: bool = True) -> Optional[Permission]:
        """
        Pega os dados de uma permissão pelo _id e atualiza
        """

        statement: Update = update(Permission) \
            .values(**dto.to_dict(), updated_at=datetime.now()) \
            .where(Permission.id == _id) \
            .returning(Permission)

        try:
            permission: Permission = await self.session.scalar(statement)
            if not permission:
                raise GenericException(f"Permissão com id {_id} não encontrado.")

            if commit:
                await self.session.commit()
                self.logger.info("Permissões atualizadas no banco.")
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao atualizar a permissão: {e}")
            await self.session.rollback()
            raise e

        return permission
