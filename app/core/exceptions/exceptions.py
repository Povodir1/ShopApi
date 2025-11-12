from fastapi import Request,status,FastAPI
from fastapi.responses import JSONResponse
from .types import *


async def bad_request_exception_handler(request: Request, exc: InvalidDataError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail})


async def not_found_exception_handler(request: Request, exc: ObjectNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail})


async def conflict_exception_handler(request: Request, exc: ObjectAlreadyExistError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.detail})


async def forbidden_exception_handler(request: Request, exc: NoPermissionsError | NoMoneyError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.detail})


async def unauthorized_exception_handler(request: Request, exc: UnauthorizedError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.detail})



def register_exception_handlers(app: FastAPI):
    """Регистрирует все пользовательские обработчики исключений в приложении."""

    app.exception_handler(InvalidDataError)(bad_request_exception_handler)
    app.exception_handler(ObjectNotFoundError)(not_found_exception_handler)
    app.exception_handler(ObjectAlreadyExistError)(conflict_exception_handler)

    app.exception_handler(NoPermissionsError)(forbidden_exception_handler)
    app.exception_handler(NoMoneyError)(forbidden_exception_handler)

    app.exception_handler(UnauthorizedError)(unauthorized_exception_handler)