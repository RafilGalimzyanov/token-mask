import aiohttp
import os

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from database.models.user_token.crud import (
    get_user_token_by_value,
    update_user_token_after_request,
)
from service.models import (
    ChatCompletionRequestDTO,
    ModelDTO,
    ErrorMessage,
    EmbeddingRequestDTO,
)
from service.routes.user.utils import (
    check_request_limit,
    check_token_limit,
    LimitExceededException,
)


ENDPOINTS = {
    "embeddings": "/embeddings",
    "chat_completions": "/chat/completions",
}
BASE_URL = os.getenv("OPENAI_BASE_URL")


def handle_openai_exception(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            return ErrorMessage(code=400, message=f"Bad Request: {e}")
        except LimitExceededException as e:
            return ErrorMessage(code=400, message=str(e))
        except HTTPException as e:
            return ErrorMessage(code=e.status_code, message=e.detail)
        except Exception as e:
            return ErrorMessage(code=400, message=f"Bad Request: {e}")

    return wrapper


@handle_openai_exception
async def chat_completions(data: ChatCompletionRequestDTO, api_key: str, db: Session):
    user_token = get_user_token_by_value(db, api_key)

    models_available = [model.name for model in user_token.models]

    if data.model not in models_available:
        raise ValueError(f"Unavailable model: {data.model}")

    check_request_limit(user_token.request_limit, user_token.request_usage)
    check_token_limit(user_token.tiktoken_limit, user_token.tokens_usage, data.messages, data.model)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user_token.openai_token}",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(BASE_URL + ENDPOINTS["chat_completions"], json=data.dict(), headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                update_user_token_after_request(user_token.id, 1, result["usage"]["total_tokens"], db)
                return result
            else:
                raise HTTPException(status_code=response.status, detail="Error from external API")


@handle_openai_exception
async def embeddings_process(data: EmbeddingRequestDTO, api_key: str, db: Session):
    user_token = get_user_token_by_value(db, api_key)

    models_available = [model.name for model in user_token.models]

    if data.model not in models_available:
        raise ValueError(f"Unavailable model: {data.model}")
    msg = [
        {"role": "system", "content": "\n".join(data.input)},
    ]

    check_request_limit(user_token.request_limit, user_token.request_usage)
    check_token_limit(user_token.tiktoken_limit, user_token.tokens_usage, msg, data.model)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {user_token.openai_token}",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            BASE_URL + ENDPOINTS["embeddings"],
            json=jsonable_encoder(data),
            headers=headers,
        ) as response:
            if response.status == 200:
                result = await response.json()
                update_user_token_after_request(user_token.id, 1, result["usage"]["total_tokens"], db)
                return result
            else:
                raise HTTPException(status_code=response.status, detail="Error from external API")
