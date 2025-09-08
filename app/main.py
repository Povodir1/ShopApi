from fastapi import FastAPI

from .api.user import router as user_router
from .api.item import router as item_router
from .api.auth import router as auth_router


app = FastAPI()

app.include_router(user_router)
app.include_router(item_router)
app.include_router(auth_router)



