from fastapi import APIRouter, HTTPException,status
from app.services import user
router = APIRouter(prefix="/users",tags=["Users"])

#вход по токену
@router.get("/me")
def get_user_me(user_id:int):
    request = user.get_user(user_id)
    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id = {user_id} not found")
    return request



#вход по токену
@router.patch("/me")
def patch_user_me():
    pass
