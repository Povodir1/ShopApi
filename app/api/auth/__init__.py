from fastapi import APIRouter
from .auth import router as auth_router
from .reset_password import router as reset_pass_router
router = APIRouter()

router.include_router(auth_router)
router.include_router(reset_pass_router)