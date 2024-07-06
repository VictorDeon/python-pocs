from typing import Optional
from datetime import datetime
from sqlalchemy import update, Update
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from ..dtos import UpdateCompanyInputDTO
from ..models import Company


class UpdateCompanyDAO:
    """
    Repositorio de manipulação da entidade de empresa
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def execute(self, cnpj: str, dto: UpdateCompanyInputDTO, commit: bool = True) -> Optional[Company]:
        """
        Pega os dados de uma empresa pelo _id e atualiza
        """

        statement: Update = update(Company).values(
            **dto.to_dict(), updated_at=datetime.now()
        ).where(Company.cnpj == cnpj).returning(Company)

        try:
            company: Company = await self.session.scalar(statement)

            if commit:
                await self.session.commit()
                self.logger.info("Empresa atualizada no banco.")
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao atualizar a empresa: {e}")
            await self.session.rollback()
            raise e

        return company
