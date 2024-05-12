from fastapi import APIRouter, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette import status

from database.models.user_token.crud import (
    check_user,
    get_user_tokens,
    get_user_token_safety,
)
from service.database_maker import get_db
from service.models import UserDTO, EmbeddingRequestDTO, ChatCompletionRequestDTO, ErrorMessage
from service.routes.user.openai_proxy import chat_completions, embeddings_process
from service.utils import check_if_error


router = APIRouter()


def get_api_key(api_key: HTTPAuthorizationCredentials = Depends(HTTPBearer()), db: Session = Depends(get_db)):
    user = check_user(api_key.credentials, db)

    if not isinstance(user, UserDTO):
        return user

    return api_key.credentials


@router.get(
    "/user_token",
    status_code=status.HTTP_200_OK,
    summary="Получение информации о пользовательском токене",
)
async def user_token(api_key: str = Depends(get_api_key), db: Session = Depends(get_db)):
    """
    """
    if isinstance(api_key, ErrorMessage):
        return check_if_error(api_key)

    return check_if_error(get_user_token_safety(db, api_key))


@router.post("/embeddings", response_model=None)
async def create_embeddings(data: EmbeddingRequestDTO, api_key: str = Depends(get_api_key), db: Session = Depends(get_db)):
    """
    """
    if isinstance(api_key, ErrorMessage):
        return check_if_error(api_key)

    return await embeddings_process(data, api_key, db)


@router.post("/chat/completions", response_model=None)
async def chat(data: ChatCompletionRequestDTO, api_key: str = Depends(get_api_key), db: Session = Depends(get_db)):
    """
    """
    if isinstance(api_key, ErrorMessage):
        return check_if_error(api_key)

    return await chat_completions(data, api_key, db)
