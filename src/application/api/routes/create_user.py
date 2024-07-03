from fastapi import status
from src.application.api.routes import router
from src.adapters.controllers import CreateUserController
from src.adapters.dtos import CreateUserInputDTO, CreateUserOutputDTO


@router.post(
    "/users",
    tags=["Banco de Dados"],
    response_model=CreateUserOutputDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um usuário."
)
async def create_user(data: CreateUserInputDTO):
    """
    Cria um usuário.
    """

    controller = CreateUserController(input=data)
    return await controller.execute()
