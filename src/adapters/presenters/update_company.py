from src.adapters.dtos import UpdateCompanyOutputDTO
from src.adapters import PresenterInterface
from src.infrastructure.databases.models import Company as CompanyModel
from .retrieve_company import RetrieveCompanyPresenter


class UpdateCompanyPresenter(PresenterInterface):
    """
    Formatação de saída da API que atualizar uma empresa.
    """

    async def present(self, model: CompanyModel) -> UpdateCompanyOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveCompanyPresenter(session=self.session)
        result = await presenter.present(model)
        return UpdateCompanyOutputDTO(company=result.company)
