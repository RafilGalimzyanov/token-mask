from pydantic import BaseModel, Field
from typing import Optional
from typing_extensions import List


class ModelAddDTO(BaseModel):
    name: str


class ModelDTO(ModelAddDTO):
    id: int


class UserTokenAddDTO(BaseModel):
    name: str
    description: str
    openai_token: str
    request_limit: int
    tiktoken_limit: int
    models: List[ModelAddDTO]


class UserTokenUpdateDTO(BaseModel):
    class Config:
        extra = "allow"


class UserTokenDTO(UserTokenAddDTO):
    id: int
    value: str
    models: List[ModelDTO]

    class Config:
        orm_mode = True


class UserTokenSecureDTO(BaseModel):
    id: int
    value: str
    name: str
    description: str
    request_limit: int
    tiktoken_limit: int
    models: List[ModelDTO]


class AdminAddDTO(BaseModel):
    token: str


class AdminDTO(AdminAddDTO):
    id: int
    name: str


class UserDTO(BaseModel):
    user_token: str


class EmbeddingRequestDTO(BaseModel):
    api_key: str
    input: list
    model: str
    encoding_format: Optional[str] = "float"

    class Config:
        extra = "allow"


class ChatCompletionRequestDTO(BaseModel):
    api_key: str
    model: str
    messages: list[dict]

    class Config:
        extra = "allow"


class ErrorMessage(BaseModel):
    code: int = Field(..., title="Error code")
    message: str = Field(..., title="Error text")
