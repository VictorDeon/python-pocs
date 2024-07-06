from sqlalchemy import insert, Insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from ..dtos import CreateCompanyInputDTO
from ..models import Company


class CreateCompanyDAO:
    """
    Repositorio de manipulação da entidade de empresa
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def execute(self, dto: CreateCompanyInputDTO, commit: bool = True) -> Company:
        """
        Cria a empresa passando como argumento os dados da mesma.
        """

        try:
            statement: Insert = insert(Company).values(**dto.to_dict()).returning(Company)
            company: Company = await self.session.scalar(statement)

            if commit:
                await self.session.commit()
                self.logger.info("Empresa inseridada no banco.")
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao criar a empresa: {e}")
            await self.session.rollback()
            raise e

        return company
