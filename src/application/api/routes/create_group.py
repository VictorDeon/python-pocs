from src.application.api.routes import router
from src.adapters.controllers import CreateGroupController
from src.adapters.dtos import CreateGroupInputDTO, CreateGroupOutputDTO


@router.post(
    "/groups",
    tags=["Banco de Dados"],
    response_model=CreateGroupOutputDTO,
    summary="Cria um grupo."
)
async def create_group(data: CreateGroupInputDTO):
    """
    Cria um grupo de usuários.
    """

    controller = CreateGroupController(input=data)
    return await controller.execute()
