from fastapi import FastAPI

from app.api.user.profile import router as user_router
from app.api.user.item import router as item_router
from app.api.user.auth import router as auth_router
from app.api.user.comments import router as comment_router
from app.api.user.basket import router as basket_router
from app.api.user.order import router as order_router
from app.api.user.favorite import router as favorite_router
from app.api.admin.items import router as admin_item_router
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
app.include_router(admin_item_router)

