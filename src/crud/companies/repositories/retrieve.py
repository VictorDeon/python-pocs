from typing import Optional
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from ..models import Company


class RetrieveCompanyDAO:
    """
    Repositorio de manipulação da entidade de empresa
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def retrieve(self, cnpj: str) -> Optional[Company]:
        """
        Pega os dados de uma empresa pelo cnpj
        """

        statement: Select = select(Company).where(Company.cnpj == cnpj)
        try:
            company: Company = await self.session.scalar(statement)
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao pegar os dados da empresa: {e}")
            raise e

        return company
