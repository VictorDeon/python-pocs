from src.application.api.routes import router
from src.adapters.controllers import CreateCompanyController
from src.adapters.dtos import CreateCompanyInputDTO, CreateCompanyOutputDTO


@router.post(
    "/companies",
    tags=["Banco de Dados"],
    response_model=CreateCompanyOutputDTO,
    summary="Cria uma empresa."
)
async def create_company(data: CreateCompanyInputDTO):
    """
    Cria uma empresa.
    """

    controller = CreateCompanyController(input=data)
    return await controller.execute()
