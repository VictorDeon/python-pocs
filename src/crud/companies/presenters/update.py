from sqlalchemy.ext.asyncio import AsyncSession
from .retrieve import RetrieveCompanyPresenter
from ..dtos import UpdateCompanyOutputDTO
from ..models import Company


class UpdateCompanyPresenter:
    """
    Formatação de saída da API que atualizar uma empresa.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, model: Company) -> UpdateCompanyOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveCompanyPresenter(session=self.session)
        company = await presenter.present(model)
        return UpdateCompanyOutputDTO(company)
