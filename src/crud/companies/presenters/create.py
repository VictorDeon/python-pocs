from sqlalchemy.ext.asyncio import AsyncSession
from .retrieve import RetrieveCompanyPresenter
from ..dtos import CreateCompanyOutputDTO
from ..models import Company


class CreateCompanyPresenter:
    """
    Formatação de saída da API que cria uma empresa.
    """

    def __init__(self, session: AsyncSession = None) -> None:
        """
        Constructor.
        """

        self.session = session

    async def present(self, model: Company) -> CreateCompanyOutputDTO:
        """
        Forma final de apresentação dos dados.
        """

        presenter = RetrieveCompanyPresenter(session=self.session)
        company = await presenter.present(model)
        return CreateCompanyOutputDTO(**company.to_dict())
