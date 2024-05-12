from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from starlette import status

from database.models.user_token.crud import check_user, get_user_tokens, get_user_token_safety
from service.database_maker import get_db
from service.models import UserDTO, EmbeddingRequestDTO, ChatCompletionRequestDTO
from service.routes.user.openai_proxy import chat_completions, embeddings_process
from service.utils import check_if_error

router = APIRouter()


@router.get("/user_token", status_code=status.HTTP_200_OK,
            summary="Получение информации о пользовательском токене")
async def user_token(
        token: str = Header(),
        db: Session = Depends(get_db)
):
    user = check_user(token, db)

    if not isinstance(user, UserDTO):
        return user

    return check_if_error(get_user_token_safety(db, token))


@router.post("/embeddings", response_model=None)
async def create_embeddings(
        data: EmbeddingRequestDTO,
        db: Session = Depends(get_db)
):
    user = check_user(data.api_key, db)

    if not isinstance(user, UserDTO):
        return user

    return await embeddings_process(data, db)


@router.post("/chat/completions", response_model=None)
async def chat(
        data: ChatCompletionRequestDTO,
        db: Session = Depends(get_db)
):
    user = check_user(data.api_key, db)

    if not isinstance(user, UserDTO):
        return user

    return await chat_completions(data, db)
