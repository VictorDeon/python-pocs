from fastapi import status
from src.routes import router
from src.engines.databases import DBConnectionHandler
from ..dtos import CreateCompanyInputDTO, CreateCompanyOutputDTO
from ..repositories import CreateCompanyDAO
from ..presenters import CreateCompanyPresenter


@router.post(
    "/companies",
    tags=["Banco de Dados"],
    response_model=CreateCompanyOutputDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma empresa."
)
async def create_company(data: CreateCompanyInputDTO):
    """
    Cria uma empresa.
    """

    async with DBConnectionHandler() as session:
        repository = CreateCompanyDAO(session=session)
        output = CreateCompanyPresenter(session=session)
        model = await repository.execute(dto=data)
        return await output.present(model)
