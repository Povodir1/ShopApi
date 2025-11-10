from app.main import app
from fastapi import Request,status
from fastapi.responses import JSONResponse
from .types import *

@app.exception_handler(InvalidDataError)
async def bad_request_exception_handler(request: Request, exc: InvalidDataError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail})

@app.exception_handler(ObjectNotFoundError)
async def not_found_exception_handler(request: Request, exc: ObjectNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail})

@app.exception_handler(ObjectAlreadyExistError)
async def conflict_exception_handler(request: Request, exc: ObjectAlreadyExistError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.detail})

@app.exception_handler(NoPermissionsError)
@app.exception_handler(NoMoneyError)
async def forbidden_exception_handler(request: Request, exc: NoMoneyError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.detail})

@app.exception_handler(UnauthorizedError)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.detail})