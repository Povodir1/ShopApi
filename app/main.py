from fastapi import FastAPI,Request,status
from fastapi.responses import JSONResponse

from app.api.user.profile import router as user_router
from app.api.user.item import router as item_router
from app.api.auth import router as auth_router
from app.api.user.comments import router as comment_router
from app.api.user.basket import router as basket_router
from app.api.user.order import router as order_router
from app.api.user.favorite import router as favorite_router
from app.api.admin.items import router as admin_item_router
from app.api.admin.users import router as admin_user_router
from app.api.admin.permissions import router as admin_permission_router
from app.api.other.image import router as image_file_router
from app.api.other.category import router as category_router
from fastapi.middleware.cors import CORSMiddleware

from app.exceptions import (InvalidDataError,NoMoneyError,
                            UnauthorizedError,NoPermissionsError,
                            ObjectAlreadyExistError,ObjectNotFoundError)


app = FastAPI(title="E-Shop API", version="1.0.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает все домены (для разработки)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все HTTP методы
    allow_headers=["*"],  # Разрешает все заголовки
)

app.include_router(user_router)
app.include_router(item_router)
app.include_router(auth_router)
app.include_router(comment_router)
app.include_router(basket_router)
app.include_router(order_router)
app.include_router(favorite_router)
app.include_router(admin_item_router)
app.include_router(admin_user_router)
app.include_router(image_file_router)
app.include_router(category_router)
app.include_router(admin_permission_router)


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