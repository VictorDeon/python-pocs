from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.formatters import paginated
from .retrieve import RetrieveCompanyPresenter
from ..models import Company
from ..dtos import ListCompaniesOutputDTO, RetrieveCompanyOutputDTO


class ListCompanyPresenter:
    """
    Formatação de saída da API que listar empresas.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, models: list[Company], limit: int = None, offset: int = None) -> ListCompaniesOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveCompanyPresenter(session=self.session)
        companies: list[RetrieveCompanyOutputDTO] = []
        for model in models:
            company = await presenter.present(model)
            companies.append(company)

        paginated_companies: list[RetrieveCompanyOutputDTO] = paginated(companies, offset, limit)

        return ListCompaniesOutputDTO(
            total=len(companies),
            companies=paginated_companies
        )
