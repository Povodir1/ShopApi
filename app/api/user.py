from fastapi import APIRouter, HTTPException,status, Depends
from app.services.user import get_user,patch_user, user_by_token
from app.schemas.user import UserPatch, UserToken,UserSchema


router = APIRouter(prefix="/users",tags=["Users"])


@router.get("/me",response_model=UserSchema)
def get_user_me(user: UserToken = Depends(user_by_token)):
    request = get_user(user.id)
    #if not request:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                        detail=f"User with id = {user.id} not found")
    return request


@router.patch("/me",response_model=UserSchema)
def patch_user_me(user_data:UserPatch,user: UserToken = Depends(user_by_token)):
    return patch_user(user.id,user_data)
