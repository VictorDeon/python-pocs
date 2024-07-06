from sqlalchemy import delete, Delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.engines.logger import ProjectLoggerSingleton
from ..models import Company


class DeleteCompanyDAO:
    """
    Repositorio de manipulação da entidade de empresa
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Constructor.
        """

        self.session = session
        self.logger = ProjectLoggerSingleton.get_logger()

    async def execute(self, cnpj: str, commit: bool = True) -> str:
        """
        Pega os dados de uma empresa pelo _id e deleta ela
        """

        statement: Delete = delete(Company).where(Company.cnpj == cnpj).returning(Company.cnpj)

        try:
            company_cnpj: str = await self.session.scalar(statement)
            if not company_cnpj:
                raise ValueError(f"Empresa com o cnpj {company_cnpj} não encontrado.")

            if commit:
                await self.session.commit()
                self.logger.info("Empresa deletada do banco.")
        except Exception as e:
            self.logger.error(f"Ocorreu um problema ao deletar a empresa: {e}")
            await self.session.rollback()
            raise e

        return company_cnpj
