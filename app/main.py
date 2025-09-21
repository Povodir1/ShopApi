from fastapi import FastAPI

from .api.user import router as user_router
from .api.item import router as item_router
from .api.auth import router as auth_router
from .api.comments import router as comment_router
from .api.basket import router as basket_router
from .api.order import router as order_router
from .api.favorite import router as favorite_router
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


