from fastapi import FastAPI,Request,status
from fastapi.responses import JSONResponse

from app.api.users.endpoints import router as user_router
from app.api.items.endpoints import router as item_router
from app.api.auth import router as auth_router
from app.api.comments.endpoints import router as comment_router
from app.api.basket.endpoints import router as basket_router
from app.api.orders.endpoints import router as order_router
from app.api.favorite.endpoints import router as favorite_router
from app.api.permissions.endpoints import router as permission_router
from app.api.categoryes.endpoints import router as category_router
from app.api.images.endpoints import router as image_router

from fastapi.middleware.cors import CORSMiddleware


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
app.include_router(category_router)
app.include_router(permission_router)
app.include_router(image_router)


