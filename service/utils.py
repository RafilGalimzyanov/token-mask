import secrets
import string

from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse, Response

from service.models import ErrorMessage


def generate_token(length=51):
    prefix = "ust-"
    charset = string.ascii_letters + string.digits
    random_part = "".join(secrets.choice(charset) for _ in range(length - len(prefix)))
    return prefix + random_part


def check_if_error(obj):
    if type(obj) is ErrorMessage:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(obj))
    else:
        if obj:
            return obj
        elif type(obj) is list:
            return obj
        else:
            return Response(status_code=status.HTTP_200_OK)
