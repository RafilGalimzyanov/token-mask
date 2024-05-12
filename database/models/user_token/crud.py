from datetime import datetime
from typing import List

from sqlalchemy.orm import Session, joinedload

from database.core import handle_database_exception
from database.models import UserTokenORM, ModelORM

from service.models import ModelAddDTO, UserDTO
from service.utils import generate_token


@handle_database_exception
def create_user_token(session: Session, name: str, description: str, openai_token: str, request_limit: int,
                      tiktoken_limit: int, models: List[ModelAddDTO]):
    for model in models:
        model_obj = session.query(ModelORM).filter(ModelORM.name == model.name).first()
        if not model_obj:
            raise ValueError(f"Model '{model.name}' not found!")

    user_token = UserTokenORM(value=generate_token(), name=name, description=description, openai_token=openai_token,
                              request_limit=request_limit, tiktoken_limit=tiktoken_limit)

    session.add(user_token)
    session.commit()

    for model in models:
        model_obj = session.query(ModelORM).filter(ModelORM.name == model.name).first()
        user_token.models.append(model_obj)

    session.commit()

    return session.query(UserTokenORM).filter_by(id=user_token.id).options(joinedload(UserTokenORM.models)).first()


@handle_database_exception
def get_user_tokens(session: Session):
    return session.query(UserTokenORM).options(joinedload(UserTokenORM.models)).all()


@handle_database_exception
def get_user_token_by_value(session: Session, value: str):
    return session.query(UserTokenORM).filter_by(value=value).options(joinedload(UserTokenORM.models)).first()


@handle_database_exception
def get_user_token_safety(session: Session, token: str):
    query = session.query(UserTokenORM).filter_by(value=token).options(joinedload(UserTokenORM.models)).first()
    if query:
        return {
            "id": query.id,
            "value": query.value,
            "request_limit": query.request_limit,
            "request_usage": query.request_usage,
            "tiktoken_limit": query.tiktoken_limit,
            "tokens_used": query.tokens_used,
            "models": query.models,
            "data_created": query.data_created
        }
    else:
        raise ValueError(f"User token '{token}' not found!")


@handle_database_exception
def update_user_token_models(session: Session, user_token: UserTokenORM, models: list):
    user_token.models.clear()

    for model_data in models:
        model_name = model_data["name"]
        if not model_name:
            raise ValueError("Model name is required to update models.")

        model = session.query(ModelORM).filter(ModelORM.name == model_name).first()
        if not model:
            raise ValueError(f"Model '{model_name}' not found!")

        user_token.models.append(model)


@handle_database_exception
def update_user_token(session: Session, user_token_id: int, attributes: dict):
    user_token = session.query(UserTokenORM).filter(UserTokenORM.id == user_token_id).first()
    if not user_token:
        raise ValueError(f"User token with id '{user_token_id}' not found!")

    for key, value in attributes.items():
        if key == "models":
            update_user_token_models(session, user_token, value)
        elif key in ("request_usage", "tokens_used"):
            ...
        elif hasattr(user_token, key):
            setattr(user_token, key, value)
        else:
            raise ValueError(f"Attribute '{key}' does not exist in UserToken!")

    user_token.data_created = datetime.utcnow()

    session.commit()

    return session.query(UserTokenORM).filter_by(id=user_token.id).options(joinedload(UserTokenORM.models)).first()


@handle_database_exception
def update_user_token_after_request(user_token_id: int, request_usage_delta: int, tokens_usage_delta: int, session: Session):
    user_token = session.query(UserTokenORM).filter(UserTokenORM.id == user_token_id).first()
    if not user_token:
        raise ValueError(f"User token with id '{user_token_id}' not found!")

    user_token.request_usage += request_usage_delta
    user_token.tokens_usage += tokens_usage_delta

    session.commit()

    return session.query(UserTokenORM).filter_by(id=user_token.id).options(joinedload(UserTokenORM.models)).first()

@handle_database_exception
def delete_user_token(session: Session, user_token_id: int):
    user_token = session.query(UserTokenORM).filter(UserTokenORM.id == user_token_id).first()
    if user_token:
        for model in user_token.models:
            user_token.models.remove(model)
        session.commit()

        session.delete(user_token)
        session.commit()
    else:
        raise ValueError(f"User token with id '{user_token_id}' not found")


@handle_database_exception
def check_user(user_token: str, session: Session) -> UserDTO:
    user_token_db = session.query(UserTokenORM).filter(UserTokenORM.value == user_token).first()
    if not user_token_db:
        raise ValueError(f"Token '{user_token}' not found in the database!")

    return UserDTO(user_token=user_token_db.value)
