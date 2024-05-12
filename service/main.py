from fastapi import FastAPI, Depends
from starlette import status
from sqlalchemy.orm import Session

from database.models import *
from database.models.admin.crud import get_admin, create_default_admin
from database.models.model.crud import add_model, delete_model, get_models
from database.models.user_token.crud import (
    create_user_token,
    get_user_tokens,
    delete_user_token,
    update_user_token,
)
from service.database_maker import get_db, SessionLocal
from service.models import UserTokenAddDTO, AdminAddDTO, ModelAddDTO, UserTokenUpdateDTO
from service.routes.user import router
from service.utils import check_if_error


tags_metadata = [
    {"name": "Admin", "description": "Функционал для администратора сервиса"},
    {"name": "User", "description": "Функционал для пользователя сервиса"},
]

app = FastAPI(
    title="Token mask service",
    openapi_tags=tags_metadata,
    description="Secure OpenAI Token Management",
    version="0.104.1",
    debug=False,
    root_path="/",
)


app.include_router(router.router, prefix="/users", tags=["User"])


@app.on_event("startup")
async def startup_event():
    with SessionLocal() as session:
        create_default_admin(session)


@app.post(
    "/user_tokens",
    tags=["Admin"],
    status_code=status.HTTP_201_CREATED,
    summary="Создание пользовательского токена",
)
async def add_user_token(
    payload: UserTokenAddDTO,
    user: AdminAddDTO = Depends(get_admin),
    db: Session = Depends(get_db),
):
    return check_if_error(create_user_token(db, **payload.__dict__))


@app.get(
    "/user_tokens",
    tags=["Admin"],
    status_code=status.HTTP_200_OK,
    summary="Получение списка пользовательских токенов",
)
async def read_user_token(user: AdminAddDTO = Depends(get_admin), db: Session = Depends(get_db)):
    return check_if_error(get_user_tokens(db))


@app.put(
    "/user_tokens/{user_token_id}",
    tags=["Admin"],
    status_code=status.HTTP_200_OK,
    summary="Изменение пользовательского токена",
)
async def put_user_token(
    user_token_id: int,
    payload: UserTokenUpdateDTO,
    user: AdminAddDTO = Depends(get_admin),
    db: Session = Depends(get_db),
):
    return check_if_error(update_user_token(db, user_token_id, payload.__dict__))


@app.delete(
    "/user_tokens/{user_token_id}",
    tags=["Admin"],
    status_code=status.HTTP_200_OK,
    summary="Удаление пользовательского токена",
)
async def del_user_token(
    user_token_id: int,
    user: AdminAddDTO = Depends(get_admin),
    db: Session = Depends(get_db),
):
    return check_if_error(delete_user_token(db, user_token_id))


@app.post(
    "/model",
    tags=["Admin"],
    status_code=status.HTTP_201_CREATED,
    summary="Добавление OpenAI модели",
)
async def add_openai_model(
    payload: ModelAddDTO,
    user: AdminAddDTO = Depends(get_admin),
    db: Session = Depends(get_db),
):
    return check_if_error(add_model(db, **payload.__dict__))


@app.get(
    "/model",
    tags=["Admin"],
    status_code=status.HTTP_200_OK,
    summary="Получение списка OpenAI моделей",
)
async def read_user_token(user: AdminAddDTO = Depends(get_admin), db: Session = Depends(get_db)):
    return check_if_error(get_models(db))


@app.delete(
    "/model",
    tags=["Admin"],
    status_code=status.HTTP_200_OK,
    summary="Удаление OpenAI модели",
)
async def del_openai_model(
    payload: ModelAddDTO,
    user: AdminAddDTO = Depends(get_admin),
    db: Session = Depends(get_db),
):
    return check_if_error(delete_model(db, **payload.__dict__))
