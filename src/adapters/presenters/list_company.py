from src.adapters.dtos import ListCompaniesOutputDTO
from src.adapters import PresenterInterface
from src.domains.entities import Company
from src.infrastructure.databases.models import Company as CompanyModel
from .retrieve_company import RetrieveCompanyPresenter


class ListCompanyPresenter(PresenterInterface):
    """
    Formatação de saída da API que listar empresas.
    """

    async def present(self, models: list[CompanyModel]) -> ListCompaniesOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveCompanyPresenter(session=self.session)
        companies: list[Company] = []
        for model in models:
            result = await presenter.present(model)
            companies.append(result.company)

        return ListCompaniesOutputDTO(companies=companies)
