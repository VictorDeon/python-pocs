from src.adapters.dtos import CreateCompanyOutputDTO
from src.adapters import PresenterInterface
from src.infrastructure.databases.models import Company as CompanyModel
from .retrieve_company import RetrieveCompanyPresenter


class CreateCompanyPresenter(PresenterInterface):
    """
    Formatação de saída da API que cria uma empresa.
    """

    async def present(self, model: CompanyModel) -> CreateCompanyOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveCompanyPresenter(session=self.session)
        result = await presenter.present(model)
        return CreateCompanyOutputDTO(company=result.company)
