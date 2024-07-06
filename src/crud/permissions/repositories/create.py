from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from sqlalchemy import insert, Insert
from ..dtos import CreatePermissionInputDTO
from ..models import Permission


class CreatePermissionDAO:
    """
    Repositorio de manipulação da entidade de permissão
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def execute(self, dto: CreatePermissionInputDTO, commit: bool = True) -> Permission:
        """
        Cria a permissão passando como argumento os dados da mesma.
        """

        try:
            statement: Insert = insert(Permission).values(**dto.to_dict()).returning(Permission)
            permission: Permission = await self.session.scalar(statement)
            if commit:
                await self.session.commit()
                self.logger.info("Permissões inseridadas no banco.")
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao criar a permissão: {e}")
            await self.session.rollback()
            raise e

        return permission
